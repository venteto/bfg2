from atproto import AtUri  # NEW
from atproto import models

# from etc.config import BFG_ENV
from etc.database import db, Post
from etc.logger import logger
from indexer.filters.accounts import ARTISTS, MUSEUMS


def operations_callback(ops: dict) -> None:
    # Here we can filter, process, run ML classification, etc.
    # After our feed alg we can save posts into our DB
    # Also, we should process deleted posts to remove them from our DB and keep it in sync

    # for example, let's create our custom feed that will contain all posts that contains alf related text

    posts_to_create = []
    for created_post in ops['posts']['created']:
        record = created_post['record']

        # print all texts just as demo that data stream works
        inlined_text = record.text.replace('\n', ' ')
        # if BFG_ENV == 'DEV':
        post_with_images = isinstance(record.embed, models.AppBskyEmbedImages.Main)
        logger.info(f'New post (with images: {post_with_images}): {inlined_text}')

        # --------------------------------------------------
        # new database column to quickly compare (offline, not deploying to
        # remote for now) feed results with Art Bots curated lists
        text = inlined_text[:40]

        # https://github.com/MarshalX/atproto/discussions/224#discussioncomment-8120157
        # this is to enable constraining a feed to a curated list of accounts
        uri = created_post['uri']
        author_did = AtUri.from_str(uri).hostname
        # --------------------------------------------------

        # only alf-related posts
        # if 'alf' in record.text.lower():

        # curated account list/dict tests

        if author_did in ARTISTS:
            reply_parent = None
            if record.reply and record.reply.parent.uri:
                reply_parent = record.reply.parent.uri

            reply_root = None
            if record.reply and record.reply.root.uri:
                reply_root = record.reply.root.uri

            post_dict = {
                'feed': 'artists',
                'text': text,
                'acct': ARTISTS.get(author_did),
                # existing fields
                'uri': created_post['uri'],
                'cid': created_post['cid'],
                'reply_parent': reply_parent,
                'reply_root': reply_root,
            }
            posts_to_create.append(post_dict)


        if author_did in MUSEUMS:
            reply_parent = None
            if record.reply and record.reply.parent.uri:
                reply_parent = record.reply.parent.uri

            reply_root = None
            if record.reply and record.reply.root.uri:
                reply_root = record.reply.root.uri

            post_dict = {
                'feed': 'museums',
                'text': text,
                'acct': MUSEUMS.get(author_did),
                # existing fields
                'uri': created_post['uri'],
                'cid': created_post['cid'],
                'reply_parent': reply_parent,
                'reply_root': reply_root,
            }
            posts_to_create.append(post_dict)

    
    """ SEE README """
    posts_to_delete = [p['uri'] for p in ops['posts']['deleted']]
    if posts_to_delete:
        Post.delete().where(Post.uri.in_(posts_to_delete))
        # if BFG_ENV == 'DEV':
        logger.info(f'Deleted from feed: {len(posts_to_delete)}')

    if posts_to_create:
        with db.atomic():
            for post_dict in posts_to_create:
                Post.create(**post_dict)
        # if BFG_ENV == 'DEV':
        logger.info(f'Added to feed: {len(posts_to_create)}')
