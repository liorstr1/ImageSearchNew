def convert_file_to_url(image_path, client):
    try:
        response = client.upload_from_path(image_path, anon=True)
        return response['link'], response['deletehash']
    except Exception as e:
        print("An error occurred:", e)
        return None, None


def delete_url_image(deletehash, client):
    try:
        return client.delete_image(deletehash)
    except Exception as e:
        return e.args
