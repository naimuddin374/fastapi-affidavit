def get_cache_key(key: str, id: int):
    return f"{key}:{id}"


# generate document file key for s3
def generate_document_file_key(account_id: int, document_id: int, file_name: str) -> str:
    result = f"{account_id}/{document_id}-{file_name.replace(' ', '_')}"
    print('document file key===', result)
    return result
