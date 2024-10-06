from Entity.ParserTcpDump import ParserTcpDump
from faststream import FastStream
from faststream.kafka import KafkaBroker
import asyncio
from dotenv import load_dotenv
import os


async def main():
    obj = ["""
    13:43:45.123456 IP 192.168.1.100.57902 > 192.168.1.50.http: Flags [P.], seq 1:97, ack 1, win 229, options [nop,nop,TS val 123456789 ecr 123456788], length 96
E..t..@.@...........P..#...."........2.P.
.................GET /resurse/1/algo?test=1 HTTP/1.1
Host: 192.168.1.50
User-Agent: curl/7.68.0
Accept: */*
""", """
13:43:45.125678 IP 192.168.1.50.http > 192.168.1.100.57902: Flags [P.], seq 1:201, ack 97, win 350, options [nop,nop,TS val 123456790 ecr 123456789], length 200
E..T./@.@....z.......P.."......."..!.......
.................HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 45

{"message": "This is the GET response"}
"""]
    parser: ParserTcpDump = ParserTcpDump()
    data = []
    urls = [
        "a/1/b",
        "a/2/b",
        "a/2/c",
        "b/2/pepe",
        "/2",
        "/5/recurso",
        "a/123e4567-e89b-12d3-a456-426614174000/b",
        "c/550e8400-e29b-41d4-a716-446655440000/d",
        "d/abc123ef-gh45-6789-ijkl-9876543210mn/x",
        "/123e4567-e89b-12d3-a456-426614174000",
        "/abc123ef-gh45-6789-ijkl-9876543210mn/recurso",
        "a/fede/b",
        "a/marco/b",
        "b/john/c",
        "c/jane/d"]
    for value in obj:
        print(value)
        print("////////////////////////////")
        parse = parser.parse_data(value)
        if (parse["request_path"] != None):
            urls.append(parse["request_path"])
        data.append(parse)
        print(parse)
        print("============================\n")
    print("\n\n==========\n\n")
    for url in urls:
        print(url)
        print("\n")

    kafka_url = os.getenv("ENV_KAFKA_URL", "")
    kafka_port = os.getenv("ENV_KAFKA_PORT", "")
    kafka = kafka_url + ":" + kafka_port
    print("kaftka is [" + kafka+"]")

    broker = KafkaBroker()
    app = FastStream(broker)

    @broker.subscriber("test")
    async def base_handler(body: bytes):
        text = body.decode()
        parse = parser.parse_data(text)
        print("\n===============================\n")
        print(parse)

    await app.run()


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
