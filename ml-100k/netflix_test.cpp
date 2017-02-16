#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define size 80000
#define rating 80000
#define users 80000
#define testrating 20000

int main()
{
    FILE *fp = fopen("movie_data.txt", "r");
    const char s[2] = "|";
    const char s1[2] = " ";
    char *token;
    int movie_data[size][19], user_ratings[rating][4], user_testratings[rating][4],movie_testusers[size][19];
    int i=0,j, count=0;
    int d=0, common_movies=0, user1_rating = 0, user2_rating = 0, l=0, common[size], current_ratings[size];
	int current_rating, max, min, t;
	float dist,total_rating=0, total_dist=0, final_dist[size],  rating_for_user, average_rating, pre_dist[size];
    if(fp != NULL)
    {
        char line[2000];
        while(fgets(line, sizeof line, fp) != NULL && i<size)
        {
            token = strtok(line, s);
                while(token!=NULL)
                {   
					if(j>0 && count < 3)
					{
						count++;
						continue;
					}
                    movie_data[i][j] = atoi(token);
//                    printf("Value of data %d %d %d ", i, j, movie_data[i][j]);  
                    j++;
                    token = strtok(NULL,s);
                } 
			count=0;
			i++;
			j=0;
        }
    }
    fclose(fp);
	i=0;
	j=0, count=0; 
	FILE *fp1 = fopen("user.txt", "r");
	if(fp1 != NULL)
    {
        char line[200];
        while(fgets(line, sizeof line, fp1) != NULL && i<rating)
        {
            token = strtok(line, s1);
                while(token!=NULL)
                {
                    user_ratings[i][j] = atoi(token);
                    j++;
                    token = strtok(NULL,s1);
                } 
			i++;
			j=0;
        }
    } 
	fclose(fp1);
	int movie_id = 1,user, movie_users[users][size],final_rating[users][size];
	for(i=0;i<users;i++)
	{
		for(j=0;j<size;j++)
		{
			movie_users[i][j]=0;
			final_rating[i][j]=0;		
		}
	}
	while(movie_id<size)
	{
		for (i=0; i<rating; i++)
			{
				if(user_ratings[i][1]==movie_id)
				{
					user = user_ratings[i][0];
					movie_users[user-1][movie_id-1]=user_ratings[i][2];
				}
			}
			movie_id++;
//			printf("akhdga");
	}
	
	i=0;
	j=0, count=0;
	movie_id = 0;
	FILE *fp2 = fopen("test_data.txt", "r");
	if(fp1 != NULL)
    {
        char line[200];
        while(fgets(line, sizeof line, fp2) != NULL && i<rating)
        {
            token = strtok(line, s1);
                while(token!=NULL)
                {
                    user_testratings[i][j] = atoi(token);
//                     printf("\nUser test %d %d %d", i, j, user_testratings[i][j]);
                    j++;
                    token = strtok(NULL,s1);
                   
                } 
			i++;
			j=0;
        }
    } 
	fclose(fp2);
//	int 
//	user, movie_users[users][size],final_rating[users][size];
	for(i=0;i<users;i++)
	{
		for(j=0;j<size;j++)
		{
			movie_testusers[i][j]=0;	
		}
	}
	while(movie_id<size)
	{
		movie_id++;
		for (i=0; i<testrating; i++)
			{
				if(user_testratings[i][1]==movie_id)
				{
					user = user_testratings[i][0];
					printf("\nTest users1 %d %d %d", user-1, movie_id-1, user_testratings[i][2]);
					movie_testusers[user-1][movie_id-1]=user_testratings[i][2];
						printf("\nTest users %d %d %d", user-1, movie_id-1, movie_testusers[user-1][movie_id-1]);		
	printf("\n Test ratings %d %d", user, movie_id);
			i=user-1;
			j = movie_id-1;
					for(int k=0; k<users; k++)
					{
					if(movie_users[k][j]!=0 && k!=i)
					{
						current_rating = movie_users[k][j];         //take rating of the user to be calculated
						 for(int m=0; m<size;m++)
						 {
						 	if(movie_users[i][m]!=0 && movie_users[k][m]!=0)
						 	{
						 		d += pow((movie_users[i][m]-movie_users[k][m]),2);
						 		user1_rating += movie_users[i][m];
						 		user2_rating += movie_users[k][m];
						 		common_movies++;
						 		printf("\ntest %d %d %d %d", i, k, m, common_movies);
						 		if(max<common_movies)
						 		{
						 			max=common_movies;
								 }
								 if(min>common_movies)
								 {
								 	min = common_movies;
								 }
							}
						 }
						 if(common_movies>0)
						 {
						 common[l]=common_movies;
						 dist = sqrt(d);
						 pre_dist[l] = dist;
						 current_ratings[l] = current_rating;
						 l++;
					}
					d=0;
					common_movies = 0;
					user1_rating =0;
					user2_rating = 0;
				}
				}
				if(l>0)
				{
				
				for(t=0; t<l ;t++)
				{
					final_dist[t] = (max/common[t])*pre_dist[t];
					rating_for_user = (current_ratings[t]/final_dist[t]);
					total_rating += rating_for_user;
					total_dist += pre_dist[t];
					printf("\nFinal rating for i & j %d %d %f %d %d %f %f",i, j,pre_dist[t] ,common[t],current_ratings[t], final_dist[t], rating_for_user);
				}
				average_rating = rating_for_user/l;
				printf("\n Total ratings %d %f %f %f", l, total_rating, total_dist, average_rating);
				
				total_dist = 0;
				total_rating = 0;
				l=0;
				}
	}
		
		}
		}
}   
