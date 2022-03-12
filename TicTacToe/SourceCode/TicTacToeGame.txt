#include <iostream>
using namespace std;

char playingBoard[9] = {'0','1','2','3','4','5','6','7','8',};

int markbox(int playernum, int position)
{
	if (playernum == 1 ){
		if(playingBoard[position] == 'X' || playingBoard[position] == 'O'){
			cout<<"\n This location is already marked by the opponent please enter another one";
			return 0;
		}
		else{
			playingBoard[position] = 'X';
			return 1;
		}
	}
	else
	if(playingBoard[position] == 'X' || playingBoard[position] == 'O'){
		cout<<"\n This location is already marked by the opponent please enter another one";
		return 0;
	}
	else{
		playingBoard[position] = 'O';
		return 1;
	}
}

void showBoard()
{
		for(int i=0;i<9;i++)
		{
      if(playingBoard[i] == 'X' || playingBoard[i] == 'O'){
        cout<< playingBoard[i] << "\t" ;
      }
      else{
        cout<< "__" << "\t" ;
      }
			if (i == 2 || i== 5 || i==8)
        cout<<"\n";
    }
}

int winCheck(){
  if (playingBoard[0] == playingBoard[1] && playingBoard[1] == playingBoard[2]){
    if(playingBoard[1] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[3] == playingBoard[4] && playingBoard[4] == playingBoard[5]){
    if(playingBoard[3] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[6] == playingBoard[7] && playingBoard[7] == playingBoard[8]){
    if(playingBoard[6] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[0] == playingBoard[3] && playingBoard[3] == playingBoard[6]){
    if(playingBoard[0] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[1] == playingBoard[4] && playingBoard[4] == playingBoard[7]){
    if(playingBoard[1] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[2] == playingBoard[5] && playingBoard[5] == playingBoard[8]){
    if(playingBoard[2] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[0] == playingBoard[4] && playingBoard[4] == playingBoard[8]){
    if(playingBoard[0] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[2] == playingBoard[4] && playingBoard[4] == playingBoard[6]){
    if(playingBoard[2] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else if (playingBoard[0] == playingBoard[3] && playingBoard[3] == playingBoard[6]){
    if(playingBoard[2] == 'X'){
      return 1;
    }
    else{
      return 2;
    }
  }
  else
		return 0;
}


int main()
{
		int p1 = 1;
    int p2 = 2;
		int boxloc;
    int matchresult = 0;
    int flag = 0;

    cout<<"Welcome to Tic Tac Toe";
    cout<<"\n Reference for input numbers for selecting position of X and O is given below";

		for(int i=1;i<5;i++)
    {
    cout<<"\n |0|1|2|";
    cout<<"\n |3|4|5|";
    cout<<"\n |6|7|8|";
		cout<< "\n Enter location of X Player " << p1 << " :- ";
		cin>> boxloc;
		while(markbox(p1, boxloc) == 0){
			cout<<"\n |0|1|2|";
	    cout<<"\n |3|4|5|";
	    cout<<"\n |6|7|8|";
			cout<< "\n Enter location of X Player " << p2 << " :- ";
			cin>> boxloc;
		}
		showBoard();

		matchresult = winCheck();
		if ( matchresult == 1 )
		{	cout<<"\n Player " << p1 << " has Won the game ! ";
			flag = 1;
			break;
		}
		else
		if ( matchresult == 2 )
		{	cout<<"\n Player " << p2 << " has Won the game ! ";
			flag = 1;
			break;
		}
    cout<<"\n |0|1|2|";
    cout<<"\n |3|4|5|";
    cout<<"\n |6|7|8|";
		cout<< "\n Enter location of O Player " << p2 << " :- ";
		cin>> boxloc;
		while(markbox(p2, boxloc) == 0){
			cout<<"\n |0|1|2|";
	    cout<<"\n |3|4|5|";
	    cout<<"\n |6|7|8|";
			cout<< "\n Enter location of O Player " << p2 << " :- ";
			cin>> boxloc;
		}
		showBoard();

		matchresult = winCheck();
		if (matchresult == 1 )
		{	cout<<"\n Player " << p1 << " has Won the game ! ";
			flag = 1;
			break;
		}
		else
		if (matchresult == 2 )
		{	cout<<"\n Player " << p2 << " has Won the game ! ";
			flag = 1;
			break;
		}
}
		if (flag == 0 )
		cout<<" \n This game is a draw ";

	return 0;
}
