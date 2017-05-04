#include <bzlib.h>
//#include "bson/BSON.h"
#include "bson.h"
#include <stdlib.h>
#include <fstream>
#include <iostream>
#include <vector>

//using namespace std;
std::vector<unsigned char> ReadFile(std::string filename)
{
	try
	{
		std::ifstream fileStream;
		fileStream.open(std::string(filename).c_str(), std::ios::binary);
		if(fileStream.is_open())
		{
			fileStream.seekg(0, std::ios::end);
			size_t fileSize = fileStream.tellg();
			fileStream.seekg(0);

			unsigned char * tempData = new unsigned char[fileSize];
			fileStream.read((char *)tempData, fileSize);
			fileStream.close();

			std::vector<unsigned char> fileData;
			fileData.insert(fileData.end(), tempData, tempData+fileSize);
			delete[] tempData;

			return fileData;
		}
		else
		{
			return std::vector<unsigned char>();
		}
	}
	catch(std::exception & e)
	{
		std::cerr << "Readfile: " << e.what() << std::endl;
		throw;
	}
}

void GameSave(char* data, int dataLength){

	unsigned char * inputData = (unsigned char*)data, *bsonData = NULL;
	unsigned int inputDataLen = dataLength, bsonDataLen = 0;

	bsonDataLen = ((unsigned)inputData[8]);
	bsonDataLen |= ((unsigned)inputData[9]) << 8;
	bsonDataLen |= ((unsigned)inputData[10]) << 16;
	bsonDataLen |= ((unsigned)inputData[11]) << 24;


	if (BZ2_bzBuffToBuffDecompress((char*)bsonData, &bsonDataLen, (char*)(inputData+12), inputDataLen-12, 0, 0)){
		std::cout << "Unable to decompress" << std::endl;
		throw;
	}
	std::cout << "Unable to decompress" << std::endl;
}


int main(void){
	int NUM = 30;
	const char name1[18] = "../0000001010.stm";
	const char name2[18] = "../580d086b00.stm";
	const char name3[18] = "../580d098500.stm";
	std::cout << "ok" << std::endl;


	std::vector<unsigned char> data;

	data = ReadFile(name1);
	std::cout << "My:" << std::endl;
	std::cout << data.size() << std::endl;
	for(int i = 0; i<NUM; i++){
		std::cout << std::hex << (int)data[i] << " ";
	}
	std::cout << std::endl;

	data = ReadFile(name2);
	std::cout << "PowderFILT:" << std::endl;
	std::cout << data.size() << std::endl;
	for(int i = 0; i<NUM; i++){
		std::cout << std::hex << (int)data[i] << " ";
	}
	std::cout << std::endl;

	data = ReadFile(name3);
	std::cout << "PowderDUST:" << std::endl;
	std::cout << data.size() << std::endl;
	for(int i = 0; i<NUM; i++){
		std::cout << std::hex << (int)data[i] << " ";
	}
	std::cout << std::endl;

	return 0;
}