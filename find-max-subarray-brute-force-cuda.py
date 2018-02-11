import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
from random import randint
import operator



def generateRandomArray(length):
    array = []
    for i in range(0, length):
        array.append(randint(-1000, 1000))
    return array

# Define CUDA function
mod = SourceModule("""
__global__ void find(int *array, int *result, int *result_end_index, int *N)  {
  int id = blockIdx.x*blockDim.x + threadIdx.x;
  int bestEndIndex = id+1;
  int bestSum = array[id];
  int currentSum = array[id];
     for(int j=id+1; j < *N; j++) {
       currentSum += array[j];
       if(currentSum > bestSum) {
         bestSum = currentSum;
         bestEndIndex = j;
       }
     }
   result[id] = bestSum;
   result_end_index[id] = bestEndIndex;
}""")
N = 1000000
N_numpy = numpy.array([N]).astype(numpy.int32)
testArray = generateRandomArray(N)
array = numpy.array(testArray).astype(numpy.int32)
result = numpy.zeros(N).astype(numpy.int32)
result_end_index = numpy.zeros(N).astype(numpy.int32)

find_func = mod.get_function("find")

# Allocate on device
array_gpu = cuda.mem_alloc(array.size * array.dtype.itemsize)
result_gpu = cuda.mem_alloc(result.size * result.dtype.itemsize)
result_end_index_gpu = cuda.mem_alloc(result_end_index.size * result_end_index.dtype.itemsize)
N_gpu = cuda.mem_alloc(N_numpy.size * N_numpy.dtype.itemsize)

# Copy from host to device
cuda.memcpy_htod(array_gpu, array)
cuda.memcpy_htod(N_gpu, N_numpy)

# Number of threads per block
threadCount = 128

# Number of blocks per grid
blockCount = int(numpy.ceil(float(N) / threadCount))

find_func(array_gpu, result_gpu, result_end_index_gpu, N_gpu, block=(threadCount, 1, 1), grid=(blockCount, 1))

# Copy result to host
cuda.memcpy_dtoh(result, result_gpu)
cuda.memcpy_dtoh(result_end_index, result_end_index_gpu)

index, value = max(enumerate(result), key=operator.itemgetter(1))

print(value, index, result_end_index[index])
