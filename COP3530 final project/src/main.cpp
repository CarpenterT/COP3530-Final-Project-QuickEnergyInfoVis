#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <chrono>
#include "Source.h"
using namespace std;

int main() {
	//load the transferData file
	ifstream inFile(".\\Intermediate_Files\\transferData.txt");
	string sortType = "";
	vector<float> unsortedData;

	if (inFile.is_open()) {
		string lineFromFile;

		//the sort type is always the first line in the file
		getline(inFile, lineFromFile);
		sortType = lineFromFile;

		while (getline(inFile, lineFromFile)) {
			unsortedData.push_back(stof(lineFromFile));
		}
	}

	inFile.close();

	vector<float> sorted;
	vector<int> timeToSort;

	//timing code from:
	//https://www.geeksforgeeks.org/measure-execution-time-function-cpp/

	//execute mergeSort
	if (sortType.compare("MergeSort") == 0) {

		auto start = chrono::high_resolution_clock::now();
		mergeSort(unsortedData, 0, unsortedData.size() - 1);
		auto stop = chrono::high_resolution_clock::now();
		auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
		timeToSort.push_back(duration.count());
		
	}
	//execute quickSort
	else if (sortType.compare("QuickSort") == 0) {
		auto start = chrono::high_resolution_clock::now();
		quickSort(unsortedData, 0, unsortedData.size() - 1);
		auto stop = chrono::high_resolution_clock::now();
		auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
		timeToSort.push_back(duration.count());
		
	}
	//execute timSort
	else if (sortType.compare("TimSort") == 0) {
		auto start = chrono::high_resolution_clock::now();
		timSort(unsortedData, unsortedData.size() - 1);
		auto stop = chrono::high_resolution_clock::now();
		auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
		timeToSort.push_back(duration.count());
		
	}
	//do all sorts (this runs all sorts for purposes of comparison)
	else if (sortType.compare("All") == 0) {
		vector<float> unsortedData2 = unsortedData;
		vector<float> unsortedData3 = unsortedData;

		auto start = chrono::high_resolution_clock::now();
		mergeSort(unsortedData, 0, unsortedData.size() - 1);
		auto stop = chrono::high_resolution_clock::now();
		auto duration = chrono::duration_cast<chrono::microseconds>(stop - start);
		timeToSort.push_back(duration.count());

		auto start1 = chrono::high_resolution_clock::now();
		quickSort(unsortedData2, 0, unsortedData2.size() - 1);
		auto stop1 = chrono::high_resolution_clock::now();
		auto duration1 = chrono::duration_cast<chrono::microseconds>(stop1 - start1);
		timeToSort.push_back(duration1.count());

		auto start2 = chrono::high_resolution_clock::now();
		timSort(unsortedData3, unsortedData3.size() - 1);
		auto stop2 = chrono::high_resolution_clock::now();
		auto duration2 = chrono::duration_cast<chrono::microseconds>(stop2 - start2);
		timeToSort.push_back(duration2.count());
	}

	sorted = unsortedData;

	//lastly, write to the returnData file
	ofstream returnFile(".\\Intermediate_Files\\returnData.txt");
	
	for (auto t : timeToSort) {
		returnFile << '\n' << t;
	}

	for (auto x : sorted) {
		returnFile << '\n' << x;
	}

	returnFile.close();

	return 0;
}