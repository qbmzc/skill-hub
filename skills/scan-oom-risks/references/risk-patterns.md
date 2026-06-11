# OOM Risk Patterns

## High-Risk Java Patterns

- `new PdfReader(InputStream)` in iText 5 reads the full stream into memory. Prefer `new PdfReader(filePath)` or a file-backed random access source when processing large PDFs.
- `ByteArrayOutputStream` followed by `toByteArray()`, Base64 encoding, or JSON response construction multiplies memory use. Prefer streaming to the response or a bounded size limit.
- Base64 input as `String` already occupies heap. Decoding to `byte[]` doubles pressure. Prefer decoder-wrapped streams and enforce strict decoded-byte limits.
- `ImageIO.read`, `Thumbnails.asBufferedImage`, `new BufferedImage`, image rotation, and watermarking can allocate large pixel arrays. Bound input bytes and pixels.
- `Graphics` and `Graphics2D` must be disposed in `finally`.
- `InputStream`, `OSSObject`, `ZipOutputStream`, `PdfReader`, `PdfDocument`, and similar resources must close on success and failure.
- `FileUtils.readFileToByteArray`, `IOUtils.toByteArray`, `IOUtils.toString(InputStream)`, and `StreamUtils.copyToByteArray` are suspect on user-controlled files.
- Zip/batch download paths need bounded file count, bounded total size, and temp-file cleanup.
- Multipart upload thresholds should spill to disk early. Confirm the multipart temp directory is a mounted volume with enough capacity.

## Configuration Patterns

- High `spring.servlet.multipart.max-file-size` or `max-request-size` expands temp-disk blast radius. It is not a heap fix by itself.
- `spring.servlet.multipart.location=/tmp` can exhaust node/container ephemeral storage during large uploads. Prefer an explicitly mounted temp directory.
- `fs.memory.base64.*` limits should remain conservative while any code path decodes Base64 to `byte[]`.
- `fs.memory.image.max-pixels` should account for multiple simultaneous `BufferedImage` instances, not only one image.
- Thread pools that mix uploads, downloads, hashing, PDF/image work, and async callbacks can amplify memory pressure. Check queue size and rejection behavior.
- K8s memory limit must leave room for heap, direct memory, metaspace, thread stacks, mmap, agents, and native libraries.

## JVM And Observability

- Add GC logs before tuning G1 parameters. For Java 8 use `-XX:+PrintGCDetails`, `-XX:+PrintGCDateStamps`, and `-Xloggc:<path>`.
- Add heap dumps for JVM OOM: `-XX:+HeapDumpOnOutOfMemoryError` and `-XX:HeapDumpPath=<mounted-path>`.
- Add `-XX:ErrorFile=<mounted-path>/hs_err_pid%p.log`.
- Use `-XX:NativeMemoryTracking=summary` only when there is a way to run `jcmd <pid> VM.native_memory summary`.
- `MaxGCPauseMillis` is a target, not a guarantee. It cannot compensate for Old Gen saturation.
- `InitiatingHeapOccupancyPercent` can be lowered to start marking earlier, but validate with GC logs.
- Do not change `G1HeapRegionSize` casually. Smaller regions lower the humongous threshold and can make more allocations humongous.

## Finding Quality Bar

For each issue, answer:

- What object/resource grows?
- How large can it get?
- How many can exist concurrently?
- What user/API path triggers it?
- Is cleanup guaranteed on exceptions?
- Is there a config limit, and is it low enough?
- What verification would prove the fix?
