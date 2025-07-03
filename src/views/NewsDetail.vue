<template>
    <div class="news-detail">
        <h1>{{ news?.name || "加载中..." }}</h1>
        <div class="news-content-wrapper news-content" v-html="htmlContent"></div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import type { NewsItem } from "@/types/news";
import "@/assets/css/news.css"; // 引入外部 CSS

const route = useRoute();
const newsId = route.params.id as string;
const news = ref<NewsItem | null>(null);
const htmlContent = ref<string>("");

const fetchNewsById = async (id: string): Promise<NewsItem | null> => {
    try {
        const response = await fetch(`/api/news/${id}`);
        if (!response.ok) throw new Error("Failed to fetch news");
        const data = await response.json();
        return data as NewsItem;
    } catch (error) {
        console.error("Error fetching news by ID:", error);
        return null;
    }
};

onMounted(async () => {
    window.scrollTo(0, 0);
    try {
        // 获取新闻元数据
        news.value = await fetchNewsById(newsId);

        // 加载 HTML 内容
        const htmlUrl = import.meta.env.DEV
            ? `/src/assets/news/${newsId}.html`
            : `/assets/news/${newsId}.html`;
        console.log("Fetching HTML from:", htmlUrl);
        const htmlResponse = await fetch(htmlUrl);
        if (!htmlResponse.ok)
            throw new Error(
                `Failed to load news content: ${htmlResponse.status} ${htmlResponse.statusText}`
            );
        const htmlText = await htmlResponse.text();
        console.log("Raw HTML:", htmlText);

        // 使用 DOMParser 解析 HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlText, "text/html");
        let blogBody = doc.querySelector(".blog-body-wrap");

        if (!blogBody) {
            console.warn(
                "blog-body-wrap not found, trying alternative selectors"
            );
            blogBody =
                doc.querySelector('div[class*="blog-body-wrap"]') ||
                doc.querySelector("body > div");
            if (blogBody) {
                console.log("Found alternative element:", blogBody.outerHTML);
            }
        }

        if (blogBody) {
            // 清理多余 <br> 和空 <p>
            let content = blogBody.outerHTML;
            content = content.replace(/<p>\s*<br\s*\/?>\s*<\/p>/g, "");
            htmlContent.value = content;
        } else {
            console.error("No blog-body-wrap or alternative found in HTML");
            htmlContent.value = "内容未找到";
        }

        console.log("Parsed HTML content:", htmlContent.value);
    } catch (error) {
        console.error("Error loading news detail:", error);
        htmlContent.value = "加载失败，请稍后重试";
    }
});
</script>

<style scoped>
.news-detail h1 {
    color: #f1c33c;
    font-size: 40px;
    text-transform: uppercase;
    -webkit-text-fill-color: rgba(0, 0, 0, 0);
    background-image: -webkit-linear-gradient(
            top,
            rgba(241, 195, 60, 0.533),
            rgba(195, 134, 0, 0.933)
        ),
        url(https://esossl-a.akamaihd.net/uploads/textures/gold.jpg);
    background-clip: text, text;
    text-align: center;
    box-sizing: border-box;
    display: block;
    line-height: 44px;
    font-weight: 700;
}

.news-content {
    max-width: 1000px;
    margin: 20px 50px 50px 50px;
    padding: 50px 20px 20px 20px;
    background-color: #121113;
    border: 1px solid #948159;
}
</style>
