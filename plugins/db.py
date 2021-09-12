from redis import Redis
from pyrogram import Client

redis = Redis('localhost', 6379)

def lpush(key:str, *data) -> bool:
    push = redis.lpush(key, *data)
    return True if len(data) == push else False


def lrange(key:str, start:int=0, end:int=-1, reverse:bool=True) -> list:
    data = [i.decode() for i in redis.lrange(key, start, end)]
    if reverse == False:
        return data
    
    else:
        data.reverse()
        return data
    
    
def llen(key:str) -> int:
    return redis.llen(key)


def lpop(key, from_end:bool=False) -> str:
    if from_end == True:
        try:
            data = lrange(key)
            data.reverse()
            pop_item = data.pop()
        
        except IndexError:
            return None
        
        else:
            if llen(key) >= 1:
                redis.delete(key)
                if len(data) >= 1:
                    data.reverse()
                    lpush(key, *data)
            
            return pop_item
    
    else:
        return redis.lpop(key).decode()
    
    
calls:dict = {}

active_calls = {}