#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2) //if not given original jpg files, then quit
    {
        printf("Usage: ./recover image");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    char filename[8];
    // new type BYTE
    typedef uint8_t BYTE;
    BYTE bytes[512];
    FILE *image; //do it here so I don't have to initialize it inside
    int counter = 0;
    while (fread(bytes, 512, 1, file) == 1) //while the file is getting read
    {
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0) //checking if jpg can be converted
        {
            if (counter > 0)
            {
                fclose(image);
            }
            //sprintf and open image so I can convert the jpges.
            sprintf(filename, "%03d.jpg", counter);
            image = fopen(filename, "w");
            if (image == NULL) //if NULL, close the file and free the space.
            {
                fclose(file);
                free(bytes);
                fprintf(stderr, "Could not create output JPG %s", filename);
                return 2;
            }
            counter ++;
        }
        //if file has been read, write it into image
        if (counter > 0)
        {
            fwrite(&bytes, 512, 1, image);
        }
    }
    fclose(file);
    fclose(image);
    return 0;
}