from mad_hatter.decorators import tool, hook
import feedparser


def parse_rss(rss_url):
	return feedparser.parse(rss_url)


def get_items(rss_url):
	items = []

	feed = parse_rss(rss_url)
	count = 0
	for item in feed['items']:
		# 获取top 10新闻
		if count >= 10:
			return items
		if item['description'] != '':
			count += 1
			items.append(f"#### [{item['title']}]({item['link']})\n    {item['description']}")

	return items


def list_to_markdown(input_list):
	markdown_string = ""
	for item in input_list:
		markdown_string += f"- {item}\n"
	return markdown_string


@tool(return_direct=True)
def get_latest_or_today_baidu_news(tool_input, bot):
	""" Get the latest baidu news.
Replies to "Latest Baidu news", "Baidu News", "百度新闻", "今日百度新闻" and similar questions.
Input is always None."""

	all_items = []
	news_urls = {
		'baidu': 'https://rss.aishort.top/?type=baidu'
	}

	for key, url in news_urls.items():
		all_items.extend(get_items(url))

	return list_to_markdown(all_items)
