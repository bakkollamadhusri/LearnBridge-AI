from typing import List
from ..models import VideoRecommendation

class VideoService:
    # Curated registry of verified, authentic educational YouTube video resources
    CURATED_VIDEOS = {
        "machine learning": [
            {
                "title": "What is Machine Learning? (Telugu Explanation)",
                "channel": "Telugu Tech / Edu",
                "url": "https://www.youtube.com/watch?v=ukzFI9rgwfU",
                "embed_url": "https://www.youtube.com/embed/ukzFI9rgwfU",
                "thumbnail_url": "https://img.youtube.com/vi/ukzFI9rgwfU/hqdefault.jpg",
                "duration": "14:20",
                "language": "Telugu",
                "description": "Comprehensive explanation of Machine Learning concepts, Supervised vs Unsupervised learning in simple Telugu."
            },
            {
                "title": "Machine Learning for Everybody – Full Course",
                "channel": "freeCodeCamp.org",
                "url": "https://www.youtube.com/watch?v=i_LwzRVP7bg",
                "embed_url": "https://www.youtube.com/embed/i_LwzRVP7bg",
                "thumbnail_url": "https://img.youtube.com/vi/i_LwzRVP7bg/hqdefault.jpg",
                "duration": "3:53:00",
                "language": "English",
                "description": "Learn Machine Learning basics, algorithms, and real-world Python implementation from freeCodeCamp."
            }
        ],
        "neural network": [
            {
                "title": "But what is a neural network? | Chapter 1, Deep Learning",
                "channel": "3Blue1Brown",
                "url": "https://www.youtube.com/watch?v=aircAruvnKk",
                "embed_url": "https://www.youtube.com/embed/aircAruvnKk",
                "thumbnail_url": "https://img.youtube.com/vi/aircAruvnKk/hqdefault.jpg",
                "duration": "19:13",
                "language": "English",
                "description": "The quintessential visual geometric explanation of neural networks, weights, biases, and activation functions by Grant Sanderson."
            }
        ],
        "pn junction": [
            {
                "title": "PN Junction Diode Working & Characteristics",
                "channel": "All About Electronics",
                "url": "https://www.youtube.com/watch?v=nO3_NfLq9w8",
                "embed_url": "https://www.youtube.com/embed/nO3_NfLq9w8",
                "thumbnail_url": "https://img.youtube.com/vi/nO3_NfLq9w8/hqdefault.jpg",
                "duration": "18:42",
                "language": "English",
                "description": "Detailed explanation of depletion region formation, forward bias, reverse bias, and barrier potential in semiconductor diodes."
            }
        ],
        "photosynthesis": [
            {
                "title": "Photosynthesis: Crash Course Biology #8",
                "channel": "CrashCourse",
                "url": "https://www.youtube.com/watch?v=sQK3Yr4Sc_k",
                "embed_url": "https://www.youtube.com/embed/sQK3Yr4Sc_k",
                "thumbnail_url": "https://img.youtube.com/vi/sQK3Yr4Sc_k/hqdefault.jpg",
                "duration": "13:15",
                "language": "English",
                "description": "Hank Green explains how plants use sunlight to produce glucose and oxygen via light-dependent reactions and the Calvin cycle."
            }
        ],
        "water cycle": [
            {
                "title": "The Water Cycle | Educational Science Video",
                "channel": "National Geographic Kids",
                "url": "https://www.youtube.com/watch?v=al-do-HGuIk",
                "embed_url": "https://www.youtube.com/embed/al-do-HGuIk",
                "thumbnail_url": "https://img.youtube.com/vi/al-do-HGuIk/hqdefault.jpg",
                "duration": "4:15",
                "language": "English",
                "description": "Clear step-by-step breakdown of Evaporation, Condensation, Precipitation, and Runoff."
            }
        ],
        "python": [
            {
                "title": "Python Full Course for Beginners [Telugu]",
                "channel": "Telugu Web Guru",
                "url": "https://www.youtube.com/watch?v=7wnove7K-ZQ",
                "embed_url": "https://www.youtube.com/embed/7wnove7K-ZQ",
                "thumbnail_url": "https://img.youtube.com/vi/7wnove7K-ZQ/hqdefault.jpg",
                "duration": "4:20:00",
                "language": "Telugu",
                "description": "Complete Python programming in Telugu covering variables, data types, functions, loops, and OOP."
            },
            {
                "title": "Python for Beginners - Full Course",
                "channel": "Programming with Mosh",
                "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                "embed_url": "https://www.youtube.com/embed/_uQrJ0TkZlc",
                "thumbnail_url": "https://img.youtube.com/vi/_uQrJ0TkZlc/hqdefault.jpg",
                "duration": "1:00:15",
                "language": "English",
                "description": "Quick, practical introduction to Python syntax, data structures, and building real projects."
            }
        ]
    }

    @classmethod
    def get_videos_for_topic(cls, topic: str, preferred_language: str = "English") -> List[VideoRecommendation]:
        topic_lower = topic.lower()
        matched = []
        
        # Check against curated verified database
        for key, vlist in cls.CURATED_VIDEOS.items():
            if key in topic_lower or topic_lower in key:
                matched.extend(vlist)
                break
                
        # If no direct match, check general keywords
        if not matched:
            if "diode" in topic_lower or "semiconductor" in topic_lower:
                matched = cls.CURATED_VIDEOS["pn junction"]
            elif "plant" in topic_lower or "biology" in topic_lower:
                matched = cls.CURATED_VIDEOS["photosynthesis"]
            elif "ai" in topic_lower or "model" in topic_lower or "data" in topic_lower:
                matched = cls.CURATED_VIDEOS["machine learning"]
            elif "code" in topic_lower or "programming" in topic_lower:
                matched = cls.CURATED_VIDEOS["python"]
                
        # Sort so preferred language matches appear first if available
        is_telugu = "telugu" in preferred_language.lower()
        
        results: List[VideoRecommendation] = []
        for item in matched:
            results.append(VideoRecommendation(
                title=item["title"],
                channel=item["channel"],
                url=item["url"],
                embed_url=item.get("embed_url"),
                thumbnail_url=item["thumbnail_url"],
                duration=item["duration"],
                language=item["language"],
                description=item["description"]
            ))
            
        if is_telugu:
            results.sort(key=lambda x: 0 if x.language.lower() == "telugu" else 1)
            
        return results
