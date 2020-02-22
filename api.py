from youtube_transcript_api import YouTubeTranscriptApi
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
            audio_descriptions: Flag to specify if audio descriptions such as `[Applause]` should be
            included in the caption list. (optional)
        """
        captions = self.yt_transcript_api.get_transcript(video_id)

        if not audio_descriptions:
            captions = [
                caption
                for caption in captions
                if not self.is_audio_description(caption['text'])
            ]

        return captions

def main():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    api.add_resource(Caption, '/<string:video_id>')

    app.run(debug=True)



if __name__ == '__main__':
    main()
