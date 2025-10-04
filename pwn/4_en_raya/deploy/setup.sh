# Check if no arguments are provided
if [ "$#" -eq 0 ] 
then    echo './setup.sh PORT EXECUTABLE_NAME DOCKER_NAME'
    exit 67
fi
# Check if the first argument (PORT) is empty
if [ "$1" = "" ]
then	echo 'err: no port given'
	exit 67
fi
# Check if the third argument (DOCKER_NAME) is empty
if [ -z "$3" ]
then    echo 'err: no docker image name given (make up a name related to your challenge)'
fi

# bin/ checking
executable="$2" # Assign the second argument (EXECUTABLE_NAME) to the variable 'executable'
if [ -f "$executable" ] # If the given executable name is a file in the current(/bin) directory
then    executable="$(basename "$executable")" # Assign the basename of 'executable' to itself
# Check if 'bin/executable' is a file
elif ! [ -f "bin/$executable" ] # neither bin/$executable nor $executable are files
then	echo 'err: no executable given'
    exit 67
fi
# Check if 'bin/flag' file exists
if ! [ -f "bin/flag" ]
then	echo 'WARNING: no flag file found in bin/flag'
fi
# Create 'rebuild.sh' if it doesn't exist, and make it executable
[ -f "rebuild.sh" ] || echo "./setup.sh '$1' '$2' '$3'" > rebuild.sh # this might break
chmod +x rebuild.sh
 # Replace occurrences of 'helloworld' with the 'executable' name in 'ctf.xinetd'
sed -i "s,helloworld,$executable," ctf.xinetd
# Stop and remove any existing Docker container with the given name
docker stop "$3"
docker rm "$3" "$3"
# Build a new Docker image with the given name
docker build -t "$3" .
# Run the Docker container with interactive terminal, 512MB memory limit, 0.5 CPU limit, restart policy, detached mode, port mapping, hostname, and name as specified
docker run -it -m 512m --cpus .5 --restart unless-stopped -d -p "0.0.0.0:$1:33333" -h "$3" --name="$3" "$3"
