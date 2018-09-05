#pragma once
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <iterator>
#include <algorithm>
#include <sstream>

using namespace std;

#ifndef TOPOLOGY_H
#define TOPOLOGY_H
	class location
	{
		public:
			location();
			virtual ~location();

			vector<vector<string>> parseNodes(string filename, char delimeter = ',');
	};
#endif // !TOPOLOGY_H



