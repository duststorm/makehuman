from mh import ArrayBuffer, Float32Array;

# build from number
f32 = Float32Array(4)

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# build from view
f32 = Float32Array(Float32Array((1.0, 2.0, 3.0, 4.0)))

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# build from buffer
f32 = Float32Array(Float32Array((1.0, 2.0, 3.0, 4.0)).buffer)

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# build from buffer with offset
f32 = Float32Array(Float32Array((1.0, 2.0, 3.0, 4.0)).buffer, 4)

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# build from buffer with offset and length
f32 = Float32Array(Float32Array((1.0, 2.0, 3.0, 4.0)).buffer, 4, 8)

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# build from sequence
f32 = Float32Array((1.0, 2.0, 3.0, 4.0))

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# item
print f32[0], f32[1], f32[2], f32[3]

# assign item
f32[1] = 5.0

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# slice
f32 = Float32Array((1.0, 2.0, 3.0, 4.0))[:2]

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

f32 = Float32Array((1.0, 2.0, 3.0, 4.0))[2:]

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# assign slice from view
f32 = Float32Array((1.0, 2.0, 3.0, 4.0))
f32[1:3] = Float32Array((5.0, 6.0))

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]

# assign slice from sequence
f32 = Float32Array((1.0, 2.0, 3.0, 4.0))
f32[1:3] = (5.0, 6.0)

print f32, f32.byteOffset, f32.byteLength, f32.length, [f for f in f32]