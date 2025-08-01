// #pragma GCC optimize ("O0")

#include "common/streamNtrip.hpp"
#include <mutex>
#include "common/trace.hpp"

using std::lock_guard;
using std::mutex;

void TcpSocket::getData()
{
    lock_guard<mutex> guard(receivedDataBufferMtx);

    const int reserve = 8192;

    receivedData.reserve(reserve);

    for (auto it = chunkList.begin(); it != chunkList.end();)
    {
        auto& chunk = *it;

        if (receivedData.size() + chunk.size() > reserve)
        {
            break;
        }

        // 		std::cout << "\nCHUNK";
        // 		printHex(std::cout, *(vector<unsigned char>*)&chunk);

        receivedData.insert(receivedData.end(), chunk.begin(), chunk.end());

        it = chunkList.erase(it);
    }
}

void TcpSocket::dataChunkDownloaded(vector<char>& dataChunk)
{
    lock_guard<mutex> guard(receivedDataBufferMtx);

    chunkList.push_back(std::move(dataChunk));
}
