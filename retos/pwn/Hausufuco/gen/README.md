gcc -o Hausufuco hausufuco.c -fno-pie -no-pie -fno-stack-protector

pwninit \
  --bin ./Hausufuco \
  --libc ./libc/glibc_2.28_no-tcache/libc.so.6 \
  --ld ./libc/glibc_2.28_no-tcache/ld-2.28.so