"""Flask app instance creation for Tech Lab 2025."""

import os
import logging
from flask import Flask, Response, jsonify
from flask_cors import CORS

from app import newsfeed
from app.utils.file_loader import load_json_files
from app.utils.redis import REDIS_CLIENT


def create_app():
    """Create a Flask app instance."""
    app = Flask("app")

    # Enable CORS for all routes to prevent frontend blockages
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configure logging for debugging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load JSON files into Redis at startup
    dataset_directory = os.path.join(os.path.dirname(__file__), "../resources/dataset/news")
    try:
        REDIS_CLIENT.save_entry("all_articles", load_json_files(dataset_directory))
        logger.info("✅ News dataset loaded into Redis.")
    except Exception as e:
        logger.error(f"❌ Error loading dataset into Redis: {e}")

    @app.route("/ping", methods=["GET"])
    def ping() -> Response:
        """Flask route to check if the server is up and running."""
        return jsonify({"message": "Pong!"}), 200

    @app.route("/get-newsfeed", methods=["GET"])
    def get_newsfeed() -> Response:
        """Flask route to get the latest newsfeed from datastore."""
        try:
            articles = newsfeed.get_all_news()
            if not articles:
                return jsonify({"error": "No articles available"}), 404

            return jsonify([article.__dict__ for article in articles]), 200
        except Exception as e:
            logger.error(f"❌ Error fetching newsfeed: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route("/get-featured-article", methods=["GET"])
    def get_featured_article() -> Response:
        """Flask route to get the featured article from datastore."""
        try:
            article = newsfeed.get_featured_news()
            if not article:
                return jsonify({"error": "No featured article found"}), 404

            return jsonify(article.__dict__), 200
        except Exception as e:
            logger.error(f"❌ Error fetching featured article: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    return app
