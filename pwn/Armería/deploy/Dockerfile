# Dockerfile for CTF (Capture The Flag) environment

# Description:
# This Dockerfile creates a CTF environment based on Ubuntu 22.04.
# It sets up a user 'ctf' and copies necessary files and directories
# to the user's home directory. It also configures xinetd and creates
# a start script.

# Example usage:
# To build the image, run:
#   docker build -t ctf .
# To run the container, run:
#   docker run -p 9999:9999 ctf

FROM ubuntu:22.04

# Update and upgrade the system
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd

# Create a new user 'ctf'
RUN useradd -m ctf

# Set the working directory to the user's home directory
WORKDIR /home/ctf

# Copy necessary files and directories to the user's home directory
RUN cp -R /lib* /home/ctf
RUN mkdir /home/ctf/usr && \
    cp -R /usr/* /home/ctf/usr

# Create device files
RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

# Copy binaries to the user's home directory
RUN mkdir /home/ctf/bin && \
    cp /bin/* /home/ctf/bin

# Copy xinetd configuration file
COPY ./ctf.xinetd /etc/xinetd.d/ctf

# Copy start script
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

# Make the start script executable
RUN chmod +x /start.sh

# Copy custom binaries to the user's home directory
COPY ./bin/ /home/ctf/

# Set ownership and permissions
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 666 /home/ctf/flag.txt

# Set the default command to run when the container starts
CMD ["/start.sh"]

# Expose port 33333
EXPOSE 33333
