from django.utils.html import escape

from twitter.apps.user.models import User


def parse_tweet(tweet):
    words = [word for word in tweet.split() if word.startswith('@') or word.startswith('#') if len(word) > 1]

    parsed_tweet = ''
    for index, word_twitter in enumerate(tweet.split()):
        new_word = escape(tweet.split()[index])
        for word in words:
            if word == word_twitter:
                if word.startswith('@'):
                    if not User.objects.filter(user__iexact=word[1:]).exists():
                        continue
                wrapped_word = f'<a href="/user/{word}" class="text-blue-400 hover:underline">{word}</a>'
                new_word = wrapped_word
        parsed_tweet += f'{new_word} '

    return parsed_tweet
