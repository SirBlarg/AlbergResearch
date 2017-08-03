#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include<time.h>
#include<random>
#include<fstream>
#include<string>
//#include<mdp_prng.h>
//#include<mdp_global_vars.h>
#include<chrono>
#include<mdp.h>
using namespace std;
//int state[3], float f_g_gg, float f_g_qq, float transition, int l
void itteratestate(int state[3], float f_g_gg, float f_g_qq, float transition, int l){ 	//int l is the index number for f_g_qq
															//int m is the index number for f_g_gg
	string fgg = to_string(f_g_gg);							//creating a naming convention for
	string fqq = to_string(f_g_qq);							//the files by making the rate parameters
	fgg.erase( fgg.find_last_not_of('0') + 1, string::npos);//string variables, and getting rid
	fqq.erase( fqq.find_last_not_of('0') + 1, string::npos);//of most of the extra 0's

	float ubar = state[0];	//pull the ubar from the state array for readability
	float dbar = state[1];	//same as above
	float g = state[2];	//And again with the gluons

	float Np = 3 + (2 * ubar) + (2 * dbar);	//Number of Partons
	float nssp_k_k1 = Np; //Because we normalized f_q_qg (This is q to quark gluon splitting
	float nssp_i1_k1 = g* f_g_qq; //Probability of a gluon becoming a u ubar pair
	float nssp_j1_k1 = g * f_g_qq; //Probability of a gluon becoming a d dbar pair (because u ubar and d dbar are equally likely to appear)
	float nssp_g_gg = g * f_g_gg; //Probability of a gluon splitting into two gluons
	float nssp_gg_g = (Np * g)  + (0.5 * g * (g-1) * f_g_gg); //Probability of two gluons contracting into one
	float nssp_k1_i1 = (ubar+2)*ubar*f_g_qq; //Probability of a u ubar pair anihilating and becoming a gluon
	float nssp_k1_j1 = (dbar+1)*dbar*f_g_qq; //Probability of a d dbar pair anihilating and becoming a gluon

	float C_0 = (nssp_k_k1 + nssp_i1_k1 + nssp_j1_k1 + nssp_g_gg + nssp_gg_g + nssp_k1_i1 + nssp_k1_j1)/(1-transition); //Computing Normalization Constant
			
	float p_k_k1 = nssp_k_k1 / C_0; //Normalizing all processes
	float p_i1_k1 = nssp_i1_k1 / C_0;
	float p_j1_k1 = nssp_j1_k1 / C_0;
	float p_g_gg = nssp_g_gg / C_0;
	float p_gg_g = nssp_gg_g / C_0;
	float p_k1_i1 = nssp_k1_i1 / C_0;
	float p_k1_j1 = nssp_k1_j1 / C_0;
	
	float nr_k_k1 = p_k_k1; 			//Setting Intervals on (0,1) that are proportional to probabilities
	float nr_i1_k1 = nr_k_k1 + p_i1_k1; 		//e.g. nr_i1_k1 will take anything between nr_k_k1 and its own value.
	float nr_j1_k1 = nr_i1_k1 + p_j1_k1; 		//Setting up intervals for dart method
	float nr_g_gg = nr_j1_k1 + p_g_gg;
	float nr_gg_g = nr_g_gg + p_gg_g;
	float nr_k1_i1 = nr_gg_g + p_k1_i1;
	float nr_k1_j1 = nr_k1_i1 + p_k1_j1;
	
	/*random_device rd;
	mt19937_64 gen(rd());
	uniform_real_distribution<> dis(0,1);
	
	float dart = dis(gen);*/
	/*mdp_int seed = 3;
	mdp_prng myRandom = new mdp_prng(seed);
	float dart = myRandom.plain();*/
	  // obtain a seed from the system clock:
	//unsigned seed1 = chrono::system_clock::now().time_since_epoch().count();

  // obtain a seed from the user:
	/*string str;
	seed_seq seed2 (str.begin(),str.end());
	minstd_rand0 g1 (seed1);  // minstd_rand0 is a standard linear_congruential_engine
	float dart = float(g1())/float(2147483647); */
	float dart = mdp_random.plain();
	
	//cout << dart;
	if (dart < nr_k_k1) {			//We through a dart at the interval (0,1)
		state[2] = state[2] + 1;	//where falling on a certain part of the
	} else if (dart < nr_i1_k1) {		//numberline indicates a certain transition.
		state[0] = state[0] + 1;	//The width of each section is weighted by
		state[2] = state[2] - 1;	//ssp, or state shift probability.
	} else if (dart < nr_j1_k1) {
		state[1] = state[1] + 1;
		state[2] = state[2] - 1;
	} else if (dart < nr_g_gg) {
		state[2] = state[2] + 1;
	} else if (dart < nr_gg_g) {
		state[2] = state[2] - 1;
	} else if (dart < nr_k1_i1) {
		state[0] = state[0] - 1;
		state[2] = state[2] + 1;
	} else if (dart < nr_k1_j1) {
		state[1] = state[1] - 1;
		state[2] = state[2] + 1;
	}
	
	ofstream history;
	history.open("history_" +  fqq + "_" + fgg + ".csv", ios_base::app);
	if(l == 0) {
		history << state[0] << "," << state[1] << "," << state[2] ;
	} else {
		
		history << "," << state[0] << "," << state[1] << "," << state[2] ;
	}
	
}
void doitterations(int itterations, int state[], float f_g_gg, float f_g_qq, float transition) {
	for( int l = 0 ; l < itterations ; l++ ){
		//int state[3], float f_g_gg, float f_g_qq, float transition, int l
		itteratestate(state, f_g_gg, f_g_qq, transition, l);
	}
	string fgg = to_string(f_g_gg);
	string fqq = to_string(f_g_qq);
	fgg.erase( fgg.find_last_not_of('0') + 1, string::npos);
	fqq.erase( fqq.find_last_not_of('0') + 1, string::npos);
	ofstream history;
	history.open("history_" +  fqq + "_" + fgg + ".csv", ios_base::app);
	history << "\n";
}

int main() {
    
	float trials;
	int itterations;
	float f_g_gg[6] = {0, 1, 2, 5, 10, 100};
	float f_g_qq[6] = {100 , 10 , 1 , 0.1 , 0.01 , 0.001};
	float transition;
	cout << "Please enter desired number of trials" << endl;
	cin >> trials;
	cout << "Please enter desired number of itterations" << endl;
	cin >> itterations;
	cout << "Please enter the probability in staying in a given state" << endl;
	cin >> transition;
	int state[3];
	int trials_t = trials;
	for(int m = 0; m < (sizeof(f_g_qq)/sizeof(*f_g_qq)) ; m++){
		for(int n = 0; n < (sizeof(f_g_gg)/sizeof(*f_g_gg)) ; n++){
			for(int i = 0; i < trials; i++){
				state[0] = 0;
				state[1] = 0;
				state[2] = 0;
				doitterations(itterations, state, f_g_gg[n], f_g_qq[m],transition);
			}
		
		}
	}
	return 0;
}
