void gadget_pop_rdi() {
    __asm__("pop %rdi; ret;");
}

void gadget_pop_rax() {
    __asm__("pop %rax; ret;");
}
