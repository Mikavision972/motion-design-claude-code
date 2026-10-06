#!/usr/bin/env python3
"""PreToolUse guard for the guardrails of AGENTS.md (local and cloud sessions).

The deny rules of .claude/settings.json match a command by its prefix only, and a deny rule cannot carry an exception.
This hook reads the tool call on stdin and refuses, whatever the spelling (env prefix, `npx --yes`, `npm exec`,
`./node_modules/.bin/hyperframes`, `bash -c "..."`, a chain with && or ;):
  - npx hyperframes@<any version but the pinned one>, npx skills;
  - hyperframes skills (any form, it overwrites the audited skills), feedback, publish, cloud, lambda, cloudrun, auth,
    upgrade, telemetry enable, --file-issue, render --skill;
  - pip install of anything but openai-whisper and playwright (also python -m pip, uv pip, pipx), and pip install
    from a requirements file, a path, a URL or another index;
  - a HeyGen, HyperFrames, ElevenLabs, Gemini/Google or OpenRouter key written in a command or a file.
Refusal: JSON permissionDecision "deny" with the reason, which Claude reads. Anything unparsable is let through to the
normal permission flow; the deny rules of settings.json still apply.
"""
import json
import os
import re
import shlex
import sys

PINNED_HYPERFRAMES = "0.8.82"
PIP_ALLOWED = {"openai-whisper", "playwright"}
HF_FORBIDDEN = {"feedback", "publish", "cloud", "lambda", "cloudrun", "auth", "upgrade", "skills"}

KEY_NAME = re.compile(
    r"^[A-Z0-9_]*(HEYGEN|HYPERFRAMES|ELEVEN|GEMINI|GOOGLE|GENAI|OPENROUTER)[A-Z0-9_]*_(KEY|TOKEN|SECRET)$|^XI_API_KEY$"
)
# NAME=value, NAME: value, "NAME": "value" with a value that looks like a real key (no placeholder).
KEY_ASSIGN = re.compile(
    r"\b([A-Z0-9_]*(?:HEYGEN|HYPERFRAMES|ELEVEN|GEMINI|GOOGLE|GENAI|OPENROUTER)[A-Z0-9_]*_(?:KEY|TOKEN|SECRET)|XI_API_KEY)"
    r"[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_\-.]{16,})"
)
# Raw key formats: Google/Gemini, OpenRouter, ElevenLabs.
KEY_VALUE = re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b|\bsk-or-v1-[0-9a-f]{40,}\b|\bsk_[0-9a-f]{48}\b")

WRAPPERS_NO_ARG = {"sudo", "time", "nohup", "command", "exec", "builtin", "stdbuf", "xargs", "nice", "ionice"}
SHELLS = {"bash", "sh", "zsh", "dash", "ksh"}
PIP_VALUE_OPTS = {
    "--root-user-action", "--progress-bar", "--upgrade-strategy", "--log", "--cache-dir", "--timeout",
    "--retries", "--python-version", "--platform", "--implementation", "--abi", "--target", "-t", "--prefix",
    "--root", "--src", "--report", "-c", "--constraint", "--proxy", "--cert", "--client-cert", "--python",
}
PIP_FORBIDDEN_OPTS = {
    "-r", "--requirement", "-e", "--editable", "-i", "--index-url", "--extra-index-url", "-f", "--find-links",
    "--trusted-host", "--no-index",
}


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Guardrail (AGENTS.md): " + reason,
    }}))
    sys.exit(0)


def check_keys(text):
    m = KEY_ASSIGN.search(text)
    if m:
        return f"never put a key in the environment or the repository ({m.group(1)}): HeyGen, ElevenLabs, Gemini and OpenRouter keys stay out of this workspace"
    if KEY_VALUE.search(text):
        return "this looks like an API key (Google/Gemini, OpenRouter or ElevenLabs format): never put a key in the environment or the repository"
    return None


def strip_heredocs(command):
    """Removes heredoc bodies (file contents, not commands); returns the bodies fed to a shell, to check them."""
    lines = command.split("\n")
    kept, shell_bodies = [], []
    i = 0
    while i < len(lines):
        line = lines[i]
        kept.append(line)
        m = re.search(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        if m and "<<<" not in line:
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != m.group(2):
                body.append(lines[i])
                i += 1
            if any(os.path.basename(t) in SHELLS for t in line[:m.start()].split()):
                shell_bodies.append("\n".join(body))
        i += 1
    return "\n".join(kept), shell_bodies


def split_segments(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    segment = []
    for tok in lexer:
        if tok and set(tok) <= set(";&|()<>\n"):
            if segment:
                yield segment
            segment = []
        else:
            segment.append(tok.strip("`"))
    if segment:
        yield segment


def strip_prefix(argv):
    """Drops VAR=value assignments and wrappers (env, sudo, time, timeout 10, nice -n 5...)."""
    i = 0
    while i < len(argv):
        tok = argv[i]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tok):
            i += 1
            continue
        base = os.path.basename(tok)
        if base == "env":
            i += 1
            while i < len(argv) and (argv[i].startswith("-") or "=" in argv[i]):
                i += 2 if argv[i] in ("-u", "--unset", "-C", "--chdir", "-S") else 1
            continue
        if base == "timeout":
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-s", "--signal", "-k", "--kill-after") else 1
            i += 1  # duration
            continue
        if base in WRAPPERS_NO_ARG:
            i += 1
            while i < len(argv) and argv[i].startswith("-"):
                i += 2 if argv[i] in ("-n", "-u", "-g", "-o", "-e", "-i", "-c", "-I", "-L") and base != "sudo" else 1
            continue
        break
    return argv[i:]


def split_pkg(spec):
    """'hyperframes@latest' -> ('hyperframes', 'latest'); '@scope/x@1' -> ('@scope/x', '1')."""
    at = spec.rfind("@")
    if at > 0:
        return spec[:at], spec[at + 1:]
    return spec, ""


def check_hf_args(args):
    pos = [a for a in args if not a.startswith("-")]
    sub = pos[0] if pos else ""
    if "--file-issue" in args or any(a.startswith("--file-issue=") for a in args):
        return "never `hyperframes ... --file-issue` (it files a public issue)"
    if sub in HF_FORBIDDEN:
        what = "skills" if sub == "skills" else sub
        return f"never `npx hyperframes {what}` unless the user asks for that exact command (the skills and the CLI are pinned and audited, nothing leaves the machine)"
    if sub == "telemetry" and "enable" in pos[1:]:
        return "telemetry stays disabled"
    if sub == "render" and any(a == "--skill" or a.startswith("--skill=") for a in args):
        return "never `render --skill=...` (that flag only attributes telemetry)"
    return None


def check_pkg_spec(spec):
    name, version = split_pkg(spec)
    if name == "skills" or name.endswith("/skills"):
        return "never `npx skills ...` (it installs unaudited third-party skills)"
    if name in ("hyperframes", "@hyperframes/cli", "@hyperframes/core") and version and version != PINNED_HYPERFRAMES:
        return f"never `npx {name}@{version}`: call the local pinned CLI, `npx hyperframes ...` ({PINNED_HYPERFRAMES})"
    return None


def check_runner(args):
    """Arguments after npx / npm exec / pnpm dlx / bunx."""
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            i += 1
            break
        if a in ("-p", "--package"):
            r = check_pkg_spec(args[i + 1]) if i + 1 < len(args) else None
            if r:
                return r
            i += 2
            continue
        if a.startswith("--package="):
            r = check_pkg_spec(a.split("=", 1)[1])
            if r:
                return r
            i += 1
            continue
        if a in ("-c", "--call"):
            if i + 1 < len(args):
                r = check_command(args[i + 1])
                if r:
                    return r
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        break
    if i >= len(args):
        return None
    r = check_pkg_spec(args[i])
    if r:
        return r
    name, _ = split_pkg(args[i])
    if name in ("hyperframes", "@hyperframes/cli"):
        return check_hf_args(args[i + 1:])
    return None


def pip_name(spec):
    return re.split(r"[\[<>=!~;@ ]", spec, 1)[0].strip().lower().replace("_", "-")


def check_pip_install(args):
    pkgs = []
    i = 0
    while i < len(args):
        a = args[i]
        opt = a.split("=", 1)[0]
        if opt in PIP_FORBIDDEN_OPTS:
            return f"pip install with `{opt}` is refused: only `pip install openai-whisper` or `pip install playwright`, from PyPI"
        if a.startswith("-"):
            i += 2 if (a in PIP_VALUE_OPTS and "=" not in a) else 1
            continue
        pkgs.append(a)
        i += 1
    bad = [p for p in pkgs if "/" in p or p.endswith((".whl", ".tar.gz", ".zip")) or pip_name(p) not in PIP_ALLOWED]
    if bad:
        return f"pip install of {', '.join(bad)} is refused: only openai-whisper and playwright may be installed with pip"
    return None


def check_argv(argv):
    for tok in argv:
        if "=" in tok:
            name, value = tok.split("=", 1)
            if KEY_NAME.match(name.removeprefix("export ").strip()) and value.strip("\"' "):
                return f"never put a key in the environment ({name}): HeyGen, ElevenLabs, Gemini and OpenRouter keys stay out of this workspace"
    argv = strip_prefix(argv)
    if not argv:
        return None
    exe = os.path.basename(argv[0])
    args = argv[1:]
    if exe in SHELLS and "-c" in args:
        idx = args.index("-c")
        return check_command(args[idx + 1]) if idx + 1 < len(args) else None
    if exe == "eval":
        return check_command(" ".join(args))
    if exe in ("npx", "bunx", "pnpx"):
        return check_runner(args)
    if exe in ("npm", "pnpm", "yarn", "bun") and args and args[0] in ("exec", "x", "dlx"):
        return check_runner(args[1:])
    if exe == "hyperframes":
        return check_hf_args(args)
    if exe == "node" and args and re.search(r"hyperframes/(dist/cli\.js|bin/)", args[0]):
        return check_hf_args(args[1:])
    if re.match(r"^pip(3(\.\d+)?)?$", exe) and args and args[0] == "install":
        return check_pip_install(args[1:])
    if re.match(r"^python(3(\.\d+)?)?$", exe) and "-m" in args:
        idx = args.index("-m")
        rest = args[idx + 1:]
        if rest[:1] == ["pip"] and rest[1:2] == ["install"]:
            return check_pip_install(rest[2:])
    if exe == "uv" and args[:2] == ["pip", "install"]:
        return check_pip_install(args[2:])
    if exe == "pipx" and args[:1] in (["install"], ["run"], ["inject"]):
        return check_pip_install(args[1:] if args[0] != "inject" else args[2:])
    return None


def check_command(command, depth=0):
    if depth > 3:
        return None
    r = check_keys(command)
    if r:
        return r
    command, shell_bodies = strip_heredocs(command)
    for body in shell_bodies:
        r = check_command(body, depth + 1)
        if r:
            return r
    try:
        segments = list(split_segments(command))
    except ValueError:
        return None
    for seg in segments:
        r = check_argv(seg)
        if r:
            return r
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    if tool == "Bash":
        r = check_command(inp.get("command", ""))
    elif tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        texts = [inp.get("content", ""), inp.get("new_string", ""), inp.get("new_source", "")]
        texts += [e.get("new_string", "") for e in inp.get("edits", []) if isinstance(e, dict)]
        r = check_keys("\n".join(t for t in texts if isinstance(t, str)))
    else:
        r = None
    if r:
        deny(r)


if __name__ == "__main__":
    main()
