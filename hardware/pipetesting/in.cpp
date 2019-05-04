// C program to implement one side of FIFO 
// This side reads first, then reads 
#include <stdio.h> 
#include <stdlib.h>
#include <string.h> 
#include <fcntl.h> 


#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <sys/stat.h> 
#include <sys/types.h> 
#include <sys/select.h>
#include <unistd.h> 

char *readline(int fd, char * buffer) {
    char c;
    int counter = 0;
    while (read(fd, &c, 1) != 0) {
        if (c == '\n') {
            break;
        }
        buffer[counter++] = c;
    }
    return buffer;
}

int main() 	
{ 	
    int fd1; 	
    fd_set set;
    struct timeval timeout;   
    int rv;
    int n;
    
    timeout.tv_sec = 0;
    timeout.tv_usec = 100000;

     // FIFO file path 	
    const char * myfifo = "/tmp/myfifo"; 	

     // Creating the named file(FIFO) 	
    // mkfifo(<pathname>,<permission>) 	
    mkfifo(myfifo, 0666); 	

    while (1) 	
    { 	
        for(int i = 0; i < 10; i++){
            char str1[50]; 	
            memset(str1, 0, 50);
            // First open in read only and read 	
            fd1 = open(myfifo,O_RDONLY); 	
            FD_ZERO(&set); /* clear the set */
            FD_SET(fd1, &set); /* add our file descriptor to the set */

            rv = select(1, &set, NULL, NULL, &timeout);
            if(rv == -1)
                perror("select"); /* an error accured */
            else if(rv == 0)
                printf("timeout"); /* a timeout occured */
            else
                readline(fd1, str1);


            // read(fd1, str1, 80); 	
            // readline(fd1, str1);
            
            // Print the read string and close 	
            printf("iteration: %d User1: %s\n", i, str1); 	
            close(fd1); 	
        }   

     } 	
    return 0; 	
}  