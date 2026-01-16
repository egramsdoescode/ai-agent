# AI Agent CLI Coding Assistant

This project is a sandboxed command line AI agent built on Google Gemini that can inspect, modify, and execute files within a constrained project directory. The agent is intentionally designed as a learning and experimentation tool rather than something safe or appropriate for real world use.

A first class goal of the project is traceability. Every file mutation performed by the agent is recorded in a structured change log so that AI driven modifications remain inspectable and reviewable.

This project is not production ready and is not intended to be used outside of educational or experimental contexts.

---

## Demo

AI Agent Demo



[AI Agent Demo](https://github.com/user-attachments/assets/2636f242-1a33-4904-8c62-4d3df3053716)



---

## High Level Overview

The agent operates with the following constraints:

* Access is restricted to a single project root
* Only explicit tool calls may read, write, or execute files
* File mutations are logged to ai-change-log.json
* The agent cannot access the network or the host system outside the project

At runtime, the agent:

1. Receives a user prompt
2. Plans a response using Gemini
3. Invokes explicit tools to inspect or modify project files
4. Records any file changes in the change log
5. Returns results to the user

This makes the agent suitable for experimenting with autonomous coding behavior while preserving visibility into what the model is actually doing.

---

## Architecture

### Core Components

```main.py```: Entry point for the CLI. Responsible for argument parsing, initializing the Gemini client, orchestrating the agent loop, and dispatching tool calls.

```prompts.py```: Defines the system and developer prompts that shape agent behavior, including tool usage rules, file access constraints, and expectations around explanation and reasoning.

```call_function.py```: Implements the tool execution layer. This file maps Gemini function calls to concrete Python functions and ensures arguments are validated and access remains limited to the project root.

Tool implementations:

* get_file_content.py
* get_files_info.py
* write_file.py
* run_python_file.py

Each tool performs a single explicit action and enforces basic safety checks such as path validation and size limits.

```config.py```: Holds centralized configuration values such as maximum file read size and output truncation limits.

---
## Example Application: Calculator

The calculator directory contains a small example application that exists solely to demonstrate the agent’s ability to inspect, modify, and extend real code.

This directory is intentionally simple and serves as a sandbox target for the agent. Changes made by the agent to files in calculator are recorded in ai-change-log.json, making it easy to correlate agent actions with concrete code modifications.

## AI Change Log

All file modifications performed by the agent are recorded in ai-change-log.json.

Each entry captures:

* The file that was modified
* File size before and after the change
* A concise summary of what changed
* The rationale for the change
* A timestamp in UTC

Example:

```
{
  "entries": [
    {
      "timestamp": "2026-01-16T13:45:12.482Z",
      "file": "pkg/calculator.py",
      "bytes_before": 192,
      "bytes_after": 2589,
      "summary": "Implement parentheses support in calculator.",
      "rationale": "User requested to fix calculator to properly process parentheses."
    }
  ]
}
```

The change log is append only and is intended to serve as an audit trail for AI driven code changes.

---

## Design Goals

* Demonstrate controlled AI assisted coding
* Make autonomous file changes auditable
* Avoid hidden side effects
* Keep the system small and inspectable

This project intentionally avoids:

* Network access
* Arbitrary shell execution
* Persistent memory outside the change log

---

## Limitations and Warnings

* Not safe for production use
* No security hardening
* Limited context window
* Python only execution environment
* Behavior depends heavily on prompt quality

This repository exists for AI learning and exploration only.

