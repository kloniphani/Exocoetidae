#include <vector>
#include <string>

#include "topology.h"

using namespace std;

int main()
{	
	location T = location();

	string filename = "..\Project Wing\Source\Topology\BackhauilingNetwork.csv";
	vector<vector<string>> dataList = T.parseNodes(filename);

	for (vector<string> vec : dataList)
	{
		for (string data : vec)
		{
			cout << data << ", ";
		}
		cout << endl;
	}

	return 0;
}
