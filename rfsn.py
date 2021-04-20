#!/usr/bin/env python
from PIL import Image
import time
'''
 Turing pattern gif using generation
 Python. Python is pretty slow though
 Take a look at the C code in the repo.
 
 No Warranty, Use at your own risk
 I won't be held responsible for any 
 damage.
'''

class chem :
   def __init__(self,a,b):
      self.a = a
      self.b = b

def cons(m,u,k):
   if m < u:
      return u
   elif m > k:
      return k
   return m

width  = 256
height = 256

dA = 1
dB = 0.5
feed = 0.0545
k = 0.062

dt = 1

grid = []
next = []

def laplaceA(x,y):
   sum = grid[x][y].a*-1.0;
   
   sum += grid[x+1][y+1].a*0.05;
   sum += grid[x+1][y-1].a*0.05;
   sum += grid[x-1][y-1].a*0.05;
   sum += grid[x-1][y+1].a*0.05;
   
   sum += grid[x][y+1].a*0.2;
   sum += grid[x][y-1].a*0.2;
   sum += grid[x-1][y].a*0.2;
   sum += grid[x+1][y].a*0.2;
   
   return sum;

def laplaceB(x,y):
   sum = grid[x][y].b*-1.0;
   
   sum += grid[x+1][y+1].b*0.05;
   sum += grid[x+1][y-1].b*0.05;
   sum += grid[x-1][y-1].b*0.05;
   sum += grid[x-1][y+1].b*0.05;
   
   sum += grid[x][y+1].b*0.2;
   sum += grid[x][y-1].b*0.2;
   sum += grid[x-1][y].b*0.2;
   sum += grid[x+1][y].b*0.2;
   
   return sum;

tm = time.localtime()
print(f"Started at \t>> {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}")

print("Forming grids \t\t>")
for x in range(width):
   grid.append([])
   next.append([])
   for y in range(height):
      
      grid[x].append(chem(1,0))
      next[x].append(chem(1,0))

print("Putting Chemical B \t->")
w_1 = int(width/2) - 64
w_2 = int(width/2) + 64

h_1 = int(height/2) - 64
h_2 = int(height/2) + 64
for i in range(w_1,w_2):
   for j in range(h_1,h_2):
      grid[i][j].b = 1

print("Computing Images \t-->")
images = []
max_iterations = 4800
iterations = 0
while (iterations < max_iterations):
   
   for x in range(1,width-1):
      for y in range(1,height-1):
         
         a = grid[x][y].a
         b = grid[x][y].b
         
         next[x][y].a = a + (dA * laplaceA(x, y) - a * b * b + feed * (1 - a)) * dt
         next[x][y].b = b + (dB * laplaceB(x, y) + a * b * b - (k + feed) * b) * dt
         
         next[x][y].a = cons(next[x][y].a, 0, 1)
         next[x][y].b = cons(next[x][y].b, 0, 1)

   if (iterations % 100 == 0):
      image = Image.new("RGB", (width,height))
      for x in range(width):
         for y in range(height):
         
            a = next[x][y].a
            b = next[x][y].b
         
            c = round((a-b)*255)
            c = cons(c,0,255)
         
            r,g,b = c,c,c
            
            image.putpixel((x,y),(r,g,b))

      images.append(image)
      
   percent = (iterations*100/max_iterations)
   print("\r Done : {:.2f} % ".format(percent), end="")
      
   grid, next = next, grid
   
   iterations += 1

images += images[:-1]

print(" : saving...")
images[0].save(f"that.gif",
           save_all=True,
           append_images=images[1:],
           optimize=False,
           duration=45,
           loop=0);

tm = time.localtime()
print(f"Ended at \t>> {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}")

print("Done.")