Feature: News Items Archive

    @auth
    Scenario: List empty archive
        Given empty "archive"
        When we get "/archive"
        Then we get list with 0 items

    @auth
    Scenario: Move item into archive
        Given empty "archive"
        And "ingest"
            """
            [{"guid": "tag:reuters.com,0000:newsml_GM1EA631K7J0", "provider": "reuters"}]
            """

        When we post to "/archive_ingest"
            """
            {
                "guid": "tag:reuters.com,0000:newsml_GM1EA631K7J0",
                "provider": "reuters"
            }
            """

        Then we get new resource
            """
            {"guid": "tag:reuters.com,0000:newsml_GM1EA631K7J0"}
            """
        And we get "archived" in "ingest/tag:reuters.com,0000:newsml_GM1EA631K7J0"
        
    @auth
    Scenario: Move item package into archive
        Given empty "archive"
        And "ingest"
            """
            [{"guid": "tag:reuters.com,2014:newsml_KBE99T04Q", "provider": "reuters"}]
            """

        When we post to "/archive_ingest"
            """
            {
                "guid": "tag:reuters.com,2014:newsml_KBE99T04Q",
                "provider": "reuters"
            }
            """

        Then we get new resource
            """
            {"guid": "tag:reuters.com,2014:newsml_KBE99T04Q"}
            """
        And we get "archived" in "ingest/tag:reuters.com,2014:newsml_KBE99T04Q"    

    @auth
    Scenario: Get archive item by guid
        Given "archive"
            """
            [{"guid": "tag:example.com,0000:newsml_BRE9A605"}]
            """

        When we get "/archive/tag:example.com,0000:newsml_BRE9A605"
        Then we get existing resource
            """
            {"guid": "tag:example.com,0000:newsml_BRE9A605"}
            """

    @auth
    Scenario: Update item
        Given "archive"
            """
            [{"_id": "xyz", "guid": "testid", "headline": "test"}]
            """

        When we patch "/archive/xyz"
            """
            {"slugline": "TEST", "urgency": 2, "version": "1"}
            """

        And we patch again
            """
            {"slugline": "TEST2", "version": "2"}
            """

        Then we get updated response
        And we get etag matching "/archive/xyz"

    @auth
    Scenario: Upload file into archive
        Given empty "archive"
        When we upload a binary file to "archive_media"
        Then we get new resource
            """
            {"guid": ""}
            """

        When we patch again
            """
            {"headline": "flower", "byline": "foo", "description_text": "flower desc"}
            """

        When we get "/archive"
        Then we get list with 1 items
            """
            {"headline": "flower", "byline": "foo", "description_text": "flower desc"}
            """

    @wip
    @auth
    Scenario: Cancel upload
        Given empty "archive"
        When we upload a binary file to "archive_media"
        And we delete it
        Then we get deleted response

