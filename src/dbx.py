import dropbox
import dropbox.files

CHUNK_SIZE = 4 * 1024 * 1024


def upload_stream(dbx, readable, dest_path):
    d = readable.read(CHUNK_SIZE)
    offset = len(d)

    session = dbx.files_upload_session_start(d)
    cursor = dropbox.files.UploadSessionCursor(session_id=session.session_id,
                                               offset=offset)
    while True:
        d = readable.read(CHUNK_SIZE)
        offset += len(d)

        if len(d) == 0:
            commit = dropbox.files.CommitInfo(path=dest_path)
            return dbx.files_upload_session_finish(d, cursor, commit)
        dbx.files_upload_session_append_v2(d, cursor)
        cursor.offset = offset


def upload_file(dbx, file_path, dest_path):
    with open(file_path, 'rb') as f:
        return upload_stream(dbx, f, dest_path)


def slurp(file_path):
    with open(file_path, 'rb') as f:
        return f.read().decode().strip()


if __name__ == '__main__':
    dbx = dropbox.Dropbox(slurp('.dbx_token'))
    print(upload_file(dbx, 'file_queries.sql', '/file_queries_there.sql'))
    # res = dbx.files_upload(
    #     b'some data', '/some_data.txt', dropbox.files.WriteMode.overwrite
    #     client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
    # )
