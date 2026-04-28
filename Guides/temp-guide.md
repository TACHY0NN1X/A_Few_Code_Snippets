# Complete Guide: Run a Local LLM on Arch Linux (Your ASUS VivoBook) Using llama.cpp

This guide covers **everything we just did**:

1. Install dependencies
2. Build the fastest practical llama.cpp for your Intel CPU
3. Download Qwen2.5 1.5B GGUF
4. Run chat locally
5. Run server on LAN
6. Connect phone GUI
7. Tune performance
8. Understand every flag

---

# 0. Why This Setup?

Your hardware:

* Intel laptop CPU with AVX2 / AVX512 capable flags
* 4GB RAM
* Arch Linux

This means:

✅ CPU is decent
⚠️ RAM is the bottleneck
✅ Linux gives better performance than Windows
✅ Small quantized models run well

Best model size for you:

```text id="j8q2rv"
1.5B to 3B quantized
```

---

# 1. Install Dependencies

Update system and install build tools:

```bash id="n4v1tx"
sudo pacman -Syu --needed \
git cmake ninja gcc openblas pkgconf ccache
```

## What each package does

| Package  | Purpose                |
| -------- | ---------------------- |
| git      | download source code   |
| cmake    | configure build        |
| ninja    | fast build system      |
| gcc      | compiler               |
| openblas | optimized math library |
| pkgconf  | helps find libraries   |
| ccache   | faster rebuilds        |

---

# 2. Download llama.cpp Source

```bash id="w7m3pa"
cd ~
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
```

This gives you the latest source.

---

# 3. Build llama.cpp (Fast Optimized Build)

## Clean old builds first

```bash id="f2k8cs"
rm -rf build
```

## Build Command

```bash id="q5n1vz"
cmake -S . -B build -G Ninja \
-DCMAKE_BUILD_TYPE=Release \
-DGGML_NATIVE=ON \
-DGGML_OPENMP=ON \
-DGGML_BLAS=ON \
-DGGML_BLAS_VENDOR=OpenBLAS \
-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON \
-DLLAMA_BUILD_SERVER=ON \
-DLLAMA_BUILD_TESTS=OFF
```

Then compile:

```bash id="x8r4md"
cmake --build build -j4
```

(`-j4` because your machine has 4 threads)

---

# 4. What These Build Flags Mean

## `-DCMAKE_BUILD_TYPE=Release`

Optimized production build.

## `-DGGML_NATIVE=ON`

Uses your CPU features automatically:

* AVX2
* FMA
* possibly AVX512

Huge speed gain.

## `-DGGML_OPENMP=ON`

Uses multiple CPU threads.

## `-DGGML_BLAS=ON`

Enable BLAS backend.

## `-DGGML_BLAS_VENDOR=OpenBLAS`

Use OpenBLAS.

Good for:

* prompt processing
* embeddings
* matrix-heavy ops

## `-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON`

Link-time optimization (LTO).

## `-DLLAMA_BUILD_SERVER=ON`

Build `llama-server`.

## `-DLLAMA_BUILD_TESTS=OFF`

Skip unnecessary tests.

---

# 5. Where Binaries Are

After build:

```bash id="m1q7tu"
ls build/bin
```

Important binaries:

| Binary           | Purpose         |
| ---------------- | --------------- |
| `llama-cli`      | local chat      |
| `llama-server`   | API server      |
| `llama-bench`    | benchmark       |
| `llama-quantize` | quantize models |

---

# 6. Create Model Directory

```bash id="p6v3zn"
mkdir -p ~/models
cd ~/models
```

Keeps models separate from source code.

---

# 7. Download Qwen2.5 1.5B GGUF

Use a quantized GGUF file (best for CPU inference).

```bash id="r2m8ka"
wget -O qwen2.5-1.5b-q4_k_m.gguf \
https://huggingface.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/Qwen2.5-1.5B-Instruct-Q4_K_M.gguf
```

Community GGUF quants are commonly hosted on Hugging Face.

---

# 8. Why This Model?

## Qwen2.5 1.5B Q4_K_M

Good balance of:

✅ quality
✅ speed
✅ low RAM use
✅ ideal for 4GB machine

---

# 9. Run Local Chat

```bash id="u7n1fd"
cd ~/llama.cpp

./build/bin/llama-cli \
-m ~/models/qwen2.5-1.5b-q4_k_m.gguf \
-t 4 \
-c 2048 \
-b 256 \
-cnv
```

---

# 10. Explain Runtime Flags

## `-m`

Model path.

## `-t 4`

Use 4 CPU threads.

## `-c 2048`

Context size = memory window.

Bigger = more RAM.

## `-b 256`

Batch size.

Good balance of speed / RAM.

## `-cnv`

Conversation mode:

* interactive chat
* auto chat formatting

---

# 11. Run As Local API Server

```bash id="z4x8pm"
cd ~/llama.cpp

./build/bin/llama-server \
-m ~/models/qwen2.5-1.5b-q4_k_m.gguf \
-t 4 \
-c 2048 \
-b 256 \
--host 0.0.0.0 \
--port 8080
```

---

# 12. Why `0.0.0.0`?

It listens on all network interfaces.

Without it:

```text id="j3p7rv"
127.0.0.1
```

means local machine only.

With `0.0.0.0`:

✅ phone on Wi-Fi can connect

---

# 13. Find Your LAN IP

```bash id="n9v2tx"
ip addr
```

Look for Wi-Fi interface:

```text id="f7k1za"
10.33.4.114
```

---

# 14. Connect From Phone

In browser:

```text id="u1x6md"
http://10.33.4.114:8080
```

API endpoint:

```text id="m8r3cp"
http://10.33.4.114:8080/v1
```

---

# 15. Phone App Settings (GPTMobile / Similar)

| Field    | Value                        |
| -------- | ---------------------------- |
| API Type | OpenAI                       |
| API URL  | `http://10.33.4.114:8080/v1` |
| API Key  | `local`                      |
| Model    | `qwen2.5-1.5b-q4_k_m`        |

---

# 16. Performance Tuning

## If RAM tight:

```text id="x5w2fd"
-c 1024
-b 128
```

## If overheating:

```text id="h2m7sa"
-t 3
```

## If stable:

```text id="k9v4pc"
-t 4
```

---

# 17. Benchmark Speed

```bash id="d6q1rt"
./build/bin/llama-bench \
-m ~/models/qwen2.5-1.5b-q4_k_m.gguf \
-t 4
```

---

# 18. Your Real Bottleneck

Not CPU.

It is:

```text id="r8m2xn"
4GB RAM
```

If upgraded to 8GB:

Massive gain.

---

# 19. Why We Chose Small Model Instead of 7B

A 7B model may run, but:

* slower
* swap pressure
* worse responsiveness
* less practical

Better to run a smaller smart model fast.

---

# 20. Best Daily Commands

## Chat

```bash id="b4t8km"
./build/bin/llama-cli \
-m ~/models/qwen2.5-1.5b-q4_k_m.gguf \
-t 4 -c 2048 -b 256 -cnv
```

## Server

```bash id="w3p9sa"
./build/bin/llama-server \
-m ~/models/qwen2.5-1.5b-q4_k_m.gguf \
-t 4 -c 2048 -b 256 \
--host 0.0.0.0 --port 8080
```

---

# 21. Future Upgrades

Try later:

* Qwen2.5 3B
* Phi-4-mini
* Gemma 4 E4B (heavier)

---

# Brutal Final Verdict

You now built a real private AI server on an old 4GB laptop.

Most people never get this far.

Your next biggest gain is **RAM upgrade**, not more compile flags.

---

# If you want, I can also make you **Part 2: Turn this into a ChatGPT clone with voice, tools, memory, and mobile UI using your laptop as the backend**.

