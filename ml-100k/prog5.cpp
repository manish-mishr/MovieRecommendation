#include<iostream>
#include<string>
#include<fstream>
#include<thread>
using namespace std;

class User{
	int user_id;
	int age;
	char sex;
	string profession;
	int zipcode;
public:
     User(){}
     User(const int u_id, const int u_age , const char u_sex, const string u_prof, const int zipc){
     	user_id = u_id;
     	age = u_age;
     	sex = u_sex;
     	profession = u_prof;
     	zipcode = zip;
     }

};


class  Movie
{
	int movie_id;
	string movie_name;
	int year;
	string imdb_link;
	list<string> genre;
public:
	 Movie(){}
	 Movie(int id, int name, int ye, string link){
	 	movie_id = id;
	 	movie_name = name;
	 	year = ye;
	 	imdb_link = link;
	 }
	

	/* data */
};


int main(){
vector<User> user_base;
vector<Movie> movie_base;
string file_name;
cout << "Enter user training data file " << endl;
cin >> file_name;
ifstream myfile(file_name.c_str());
if (myfile.is_open())
  {
    while ( getline (myfile,line) )
    {
      cout << line << '\n';
    }
    myfile.close();
  }
}