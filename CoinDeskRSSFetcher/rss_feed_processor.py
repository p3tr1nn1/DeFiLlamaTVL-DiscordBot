import fetcher_coindesk_rss
import fetcher_defiant_rss
import fetcher_investing_rss
import set_discord_queue

def main():
    # Call the main functions of each script
    fetcher_coindesk_rss.main()
    fetcher_defiant_rss.main()
    fetcher_investing_rss.main()
    set_discord_queue.main()

if __name__ == "__main__":
    main()
