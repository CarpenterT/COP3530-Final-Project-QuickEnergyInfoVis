#pragma once
#include <vector>
#include <iostream>
#include <chrono>
#include <random>

using namespace std::chrono;
using namespace std;
// size of subvectors being sorted in timSort
const int RUN = 32;

void printVector(vector<float> v)
{
	for (float f : v)
	{
		cout << f << " ";
	}
}

// use in mergeSort and timSort
void merge(vector<float>& data, int left, int mid, int right)
{
	int n1 = mid - left + 1;
	int n2 = right - mid;
	vector<float> x;
	vector<float> y;
	// input data into two separate vectors which should each be already sorted
	for (int i = 0; i < n1; i++)
		x.push_back(data[left + i]);
	for (int j = 0; j < n2; j++)
		y.push_back(data[mid + 1 + j]);
	int i = 0;
	int j = 0;
	int k = left;

	// while both are nonempty, merge by pushing back the smaller leading element
	while (i < n1 && j < n2)
	{
		if (x[i] <= y[j])
		{
			data[k] = x[i];
			i++;
		}
		else
		{
			data[k] = y[j];
			j++;
		}
		k++;
	}
	// if either subvector is empty, input remaining elements in nonempty subvector
	while (i < n1)
	{
		data[k] = x[i];
		i++;
		k++;
	}
	while (j < n2)
	{
		data[k] = y[j];
		j++;
		k++;
	}
}

void mergeSort(vector<float>& data, int left, int right)
{
	if (left < right)
	{
		int mid = (left + right) / 2;
		mergeSort(data, left, mid);
		mergeSort(data, mid + 1, right);
		merge(data, left, mid, right);
	}
}

// use in quickSort
int partition(vector<float>& data, int low, int high)
{
	int pivot = data[low];
	int up = low;
	int down = high;

	while (up < down)
	{
		// shift up index to the right until reaching a value > pivot
		for (int i = up; i < high; i++)
		{
			if (data[up] > pivot)
				break;
			up++;
		}
		// shift down index to the left until reaching a value < pivot
		for (int i = high; i > low; i--)
		{
			if (data[down] < pivot)
				break;
			down--;
		}
		// swap up and down indices if they haven't crossed yet, basically swap every time except the last iteration
		if (up < down)
			swap(data[up], data[down]);
	}
	// once up and down indices have crossed, put the pivot in the right position
	swap(data[low], data[down]);
	// return new index of pivot
	return down;
}

void quickSort(vector<float>& data, int low, int high)
{
	if (low < high)
	{
		int pivot = partition(data, low, high);
		quickSort(data, low, pivot - 1);
		quickSort(data, pivot + 1, high);
	}
}

/*
void selectionSort(vector<float>& data, int size)
{
	for (int i = 0; i < size - 1; i++)
	{
		int min_index = i;
		for (int j = i + 1; j < size; j++)
		{
			if (data[j] < data[min_index])
				min_index = j;
		}
		swap(data[min_index], data[i]);
	}
}
*/

// use in timSort
void insertionSort(vector<float>& data, int left, int right)
{
	for (int i = left + 1; i <= right; i++)
	{
		float key = data[i];
		int j = i - 1;
		// j >= 0 has to come first so it is checked before key < data[j]
		while (j >= left && key < data[j])
		{
			// shift indices while finding correct position
			data[j + 1] = data[j];
			j--;
		}
		// insert in correct position in sorted portion of the vector
		data[j + 1] = key;
	}
}

void timSort(vector<float>& data, int size)
{
	// perform insertion sort on subvectors of size RUN
	for (int i = 0; i < size; i += RUN)
		// use min function to account for when the end of the vector is reached
		insertionSort(data, i, min(i + RUN - 1, size));

	// merge sorted subvectors
	for (int i = RUN; i < size; i *= 2)
	{
		for (int left = 0; left < size; left += 2 * i)
		{
			int mid =  left + i - 1;
			// use min function to account for when the end of the vector is reached
			int right = min(left + 2 * i - 1, size);

			// merge subvectors
			if (mid < right)
				merge(data, left, mid, right);
		}
	}
}
/*
int main()
{
	random_device rnd_device;
	mt19937 mersenne_engine{rnd_device()};
	uniform_int_distribution<int> dist{1, 100};

	auto gen = [&dist, &mersenne_engine]() {
		return dist(mersenne_engine);
	};

	// generate vectors for comparison
	vector<float> v1(200000);
	vector<float> v2(200000);
	vector<float> v3(200000);
	generate(begin(v1), end(v1), gen);
	generate(begin(v2), end(v2), gen);
	generate(begin(v3), end(v3), gen);
	
	//printVector(v1);
	cout << endl;

	// compare algs
	auto start1 = high_resolution_clock::now();
	mergeSort(v1, 0, v1.size() - 1);
	auto stop1 = high_resolution_clock::now();
	auto duration1 = duration_cast<microseconds>(stop1 - start1);
	//printVector(v1);
	cout << endl;
	cout << "MergeSort Time: " << duration1.count() << " microseconds" << endl;

	//printVector(v2);
	cout << endl;
	auto start2 = high_resolution_clock::now();
	quickSort(v2, 0, v2.size() - 1);
	auto stop2 = high_resolution_clock::now();
	auto duration2 = duration_cast<microseconds>(stop2 - start2);
	//printVector(v2);
	cout << endl;
	cout << "QuickSort Time: " << duration2.count() << " microseconds" << endl;

	//printVector(v3);
	cout << endl;
	auto start3 = high_resolution_clock::now();
	timSort(v3, v3.size() - 1);
	auto stop3 = high_resolution_clock::now();
	auto duration3 = duration_cast<microseconds>(stop3 - start3);
	//printVector(v3);
	cout << endl;
	cout << "TimSort Time: " << duration3.count() << " microseconds" << endl;
}
*/