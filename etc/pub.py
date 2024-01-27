#!/usr/bin/env python3

import argparse
from atproto import Client, models

import config


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script for publishing and unpublishing feeds.')
    parser.add_argument('feed', help='Feed ID to publish/delete.')
    parser.add_argument(
        '--drop',
        action='store_true',
        help='Delete/unpublish feed.')
    return parser.parse_args()


def main():
    args = parse_args()

    for feed in config.FEEDS:
        if feed.record_name == args.feed:
            break
    else:
        print(
            f'Could not find feed `{args.feed}` in: {", ".join(f.record_name for f in config.FEEDS)}')
        return

    avatar_blob = None
    # TODO: Add icon.
    # if AVATAR_PATH:
    #    with open(AVATAR_PATH, 'rb') as f:
    #        avatar_data = f.read()
    #        avatar_blob = client.com.atproto.repo.upload_blob(avatar_data).blob

    client = Client()
    client.login(config.HANDLE, config.PASSWORD)
    # if args.unpublish:
    if args.drop:
        response = client.com.atproto.repo.delete_record(
            models.ComAtprotoRepoDeleteRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedGenerator,
                rkey=feed.record_name,
            )
        )
        print('Success:', response)
    else:
        response = client.com.atproto.repo.put_record(
            models.ComAtprotoRepoPutRecord.Data(
                repo=client.me.did,
                collection=models.ids.AppBskyFeedGenerator,
                rkey=feed.record_name,
                record=models.AppBskyFeedGenerator.Main(
                    did=config.SERVICE_DID,
                    display_name=feed.display_name,
                    description=feed.description,
                    avatar=avatar_blob,
                    created_at=client.get_current_time_iso(),
                )))
        print('response:', response)
        print()
        print('feed URI:', response.uri)


if __name__ == '__main__':
    main()
