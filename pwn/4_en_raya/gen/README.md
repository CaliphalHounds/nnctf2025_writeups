gcc 4enraya.c -o 4enraya \
  -O0 \
  -no-pie \                           
  -fno-stack-protector \              
  -Wl,-z,relro -Wl,-z,lazy \          
  -Wl,-z,noexecstack \ 