import NewsCard from "@/components/NewsCard";
import NewsFeed from "@/components/NewsFeed";
import { useState, useEffect } from "react";
import { Article } from "@/utils/types";
import FeaturedNewsCard from "@/components/FeaturedNews";

export default function News() {
    const [articles, setArticles] = useState<Article[]>([]);
    const [featuredArticle, setFeaturedArticle] = useState<Article | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const backendUrl = "http://localhost:8000";
    
                // Fetch Featured Article
                const featuredResponse = await fetch(`${backendUrl}/get-featured-article`);
                if (!featuredResponse.ok) throw new Error("Failed to fetch featured article");
                const featuredData = await featuredResponse.json();
                setFeaturedArticle(featuredData);
    
                // Fetch News Feed Articles
                const newsResponse = await fetch(`${backendUrl}/get-newsfeed`);
                if (!newsResponse.ok) throw new Error("Failed to fetch newsfeed");
                const newsData = await newsResponse.json();
                setArticles(newsData);
    
            } catch (error) {
                console.error("Error fetching news data:", error);
            }
        };
    
        fetchData();
    }, []);    

    return (
        <div>
            <div className="grid grid-cols-4 space-x-2 space-y-2 pt-2">
                <div className="col-span-4 lg:col-span-3">
                    {featuredArticle && <FeaturedNewsCard article={featuredArticle} />}
                    <NewsFeed articles={articles} />
                </div>
                <div className="hidden lg:block col-span-1 overflow-hidden border-l border-slate-300">
                    <div className="flex flex-col gap-4 divide-y divide-slate-300 space-x-2">
                        {articles.slice(0, 6).map((article, i) => (
                            <NewsCard key={`${article.title}_${i}`} article={article} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
