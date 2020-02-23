from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS


class Caption(Resource):

    def __init__(self, yt_transcript_api=YouTubeTranscriptApi):
        self.yt_transcript_api = yt_transcript_api

    @staticmethod
    def is_audio_description(text: str):
        """Determine if `text` is an audio description.
        """
        return text.startswith('[') and text.endswith(']')

    def get(
        self,
        video_id: str,
        audio_descriptions: bool = False
    ):
        """Get captions for `video_id`.

        Arguments:
            video_id: YouTube video ID.
        """
        try:
            captions = self.yt_transcript_api.get_transcript(video_id)
        except TranscriptsDisabled:
            return dict(error='Transcript is not available for this video.'), 404
        except VideoUnavailable:
            return dict(error='Video is unavailable.'), 404

        words = [{'word':word, 'time':caption['start']} for caption in captions for word in caption['text'].split()]

        return words

def main():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    api.add_resource(Caption, '/<string:video_id>')

    app.run(debug=True)



if __name__ == '__main__':
    main()
