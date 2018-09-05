#include "topology.h"

location::location()
{
}


location::~location()
{
}

vector<vector<string>> parseNodes(string filename, char delimeter = ',')
{
	ifstream file(filename);
	vector<vector<string>> dataList;
	string line = "";

	while (getline(file, line))
	{
		vector<string> vec;
		istringstream tokenStream(line);
		string token;

		while (getline(tokenStream, token, delimeter))
		{
			vec.push_back(token);
		}

		dataList.push_back(vec);
	}
	file.close();
	return dataList;
}