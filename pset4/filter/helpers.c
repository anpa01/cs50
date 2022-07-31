#include "helpers.h"
#include "math.h"
#include "stdio.h"
//had to add math for rounding
// Convert image to grayscale
//created temp for blur
typedef struct
{
    int red;
    int blue;
    int green;
    float counter; //i added this and made it a float because of rounding issues
}
temp;
// in grayscale, I wanted to take the average and make it all that form of color
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int average = round((red + blue + green) / 3.0); //
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
    return;
}

// Convert image to sepia
// in sepia I used a formula to make them a version of sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int sepiaRed = round((0.393 * red) + (0.769 * green) + (0.189 * blue));
            int sepiaGreen = round((0.349 * red) + (0.686 * green) + (0.168 * blue));
            int sepiaBlue = round((0.272 * red) + (0.534 * green) + (0.131 * blue));
            //made sure if it exceeded 255 it would be 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
        }
    }
    return;
}

// Reflect image horizontally
// in reflect I used a temporary array and switched the two
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //using temp so I could switch them
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1]; //
            image[i][width - j - 1] = temp; //
        }
    }
    return;
}

// Blur image
//in blur I took the average of them all by using if statements to make sure I didn't take and average of one outside the image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    temp temp1[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp1[i][j].red = image[i][j].rgbtRed;
            temp1[i][j].blue = image[i][j].rgbtBlue;
            temp1[i][j].green = image[i][j].rgbtGreen;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int totalRed = temp1[i][j].red;
            int totalGreen = temp1[i][j].green;
            int totalBlue = temp1[i][j].blue;
            temp1[i][j].counter = 1.0; // i need this so I can divide by the proper number to get the proper average
            if (i - 1 >= 0)
            {
                totalRed = totalRed + temp1[i - 1][j].red;
                totalGreen = totalGreen + temp1[i - 1][j].green;
                totalBlue = totalBlue + temp1[i - 1][j].blue;
                temp1[i][j].counter ++;
            }
            if (i + 1 < height)
            {
                totalRed = totalRed + temp1[i + 1][j].red;
                totalGreen = totalGreen + temp1[i + 1][j].green;
                totalBlue = totalBlue + temp1[i + 1][j].blue;
                temp1[i][j].counter ++;
            }
            if (j - 1 >= 0)
            {
                totalRed = totalRed + temp1[i][j - 1].red;
                totalGreen = totalGreen + temp1[i][j - 1].green;
                totalBlue = totalBlue + temp1[i][j - 1].blue;
                temp1[i][j].counter ++;
            }
            if (j + 1 < width)
            {
                totalRed = totalRed + temp1[i][j + 1].red;
                totalGreen = totalGreen + temp1[i][j + 1].green;
                totalBlue = totalBlue + temp1[i][j + 1].blue;
                temp1[i][j].counter ++;
            }
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                totalRed = totalRed + temp1[i - 1][j - 1].red;
                totalGreen = totalGreen + temp1[i - 1][j - 1].green;
                totalBlue = totalBlue + temp1[i - 1][j - 1].blue;
                temp1[i][j].counter ++;
            }
            if (i - 1 >= 0 && j + 1 < width)
            {
                totalRed = totalRed + temp1[i - 1][j + 1].red;
                totalGreen = totalGreen + temp1[i - 1][j + 1].green;
                totalBlue = totalBlue + temp1[i - 1][j + 1].blue;
                temp1[i][j].counter ++;
            }
            if (i + 1 < height && j - 1 >= 0)
            {
                totalRed = totalRed + temp1[i + 1][j - 1].red;
                totalGreen = totalGreen + temp1[i + 1][j - 1].green;
                totalBlue = totalBlue + temp1[i + 1][j - 1].blue;
                temp1[i][j].counter ++;
            }
            if (i + 1 < height && j + 1 < width)
            {
                totalRed = totalRed + temp1[i + 1][j + 1].red;
                totalGreen = totalGreen + temp1[i + 1][j + 1].green;
                totalBlue = totalBlue + temp1[i + 1][j + 1].blue;
                temp1[i][j].counter ++;
            }
            // got the average of them
            int averageRed = round((totalRed) / (temp1[i][j].counter));
            int averageGreen = round((totalGreen) / (temp1[i][j].counter));
            int averageBlue = round((totalBlue) / (temp1[i][j].counter));
            image[i][j].rgbtRed = averageRed;
            image[i][j].rgbtBlue = averageBlue;
            image[i][j].rgbtGreen = averageGreen;
        }
    }
}
