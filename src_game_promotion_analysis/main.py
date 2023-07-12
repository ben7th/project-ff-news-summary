from src.extraction import extract_webpage_content
from src.summarization import summarize_content
from src.analysis import analyze_content
from src.tracing import trace_information
from src.timeline import organize_timeline
from src.storage import save_data
from src.visualization import visualize_data


def main():
    # Step 1: 获取网页地址 - 手工操作，不整合进流程
    # scripts.get_webpage_urls

    #   Step 1-1: JSON 信息入库 - 手工操作，不整合进流程
    #   scripts.save_json_to_db

    #   Step 1-2: 提取 title, source, languages 信息 - 手工操作，不整合进流程
    #   scripts.update_db_items_title

    # Step 2: 使用 pyppeteer 抓取网页原始信息 - 手工操作，不整合进流程
    # scripts.pyppeteer_crawler

    # Step 3: 重点摘要和信息提取 - 手工操作，不整合进流程
    # scripts.clean_html_content_by_goose - 使用 goose 提取，保存到 goose_article
    # scripts.llm_extract_summary - 使用 llm 提取，保存到 llm_summary
    # [未使用] scripts.clean_html_content_by_boilerpy - 效果不理想

    # # Step 4: 信息向量化与聚类分析
    # 

    # # Step 5: 信息溯源方法
    # 

    # # Step 6: 组织时间线
    # 

    # # Step 7: 数据存储
    # 

    # # Step 8: 展示方法
    # 
    
    return


if __name__ == "__main__":
    main()
