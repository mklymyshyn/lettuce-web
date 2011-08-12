Feature: Browser and Assert
	Scenario: Test open_url
        Open url
        Open url without tree
        Open url by shortcut

    Scenario: Test assert_response_code
        Open url with code 200
        Open url with code 304
    
    Scenario: Test assert_link
        Check that link exist
        Check that link doesn't exist
    
    Scenario: Test assert_contains
        Check that body contains string
        Check that body doesn't contain string
        Check that body contain string exactly 2 times
