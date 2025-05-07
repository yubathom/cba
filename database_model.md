# Baseball Database Model

Below is a database model diagram for the baseball statistics tracking system based on the CSV output files.

```mermaid
erDiagram
    PLAYER ||--o{ BATTING : performs
    PLAYER ||--o{ PITCHING : performs
    PLAYER ||--o{ FIELDING : performs
    TEAM ||--o{ PLAYER : has
    ROUND ||--o{ BATTING : has
    ROUND ||--o{ PITCHING : has
    ROUND ||--o{ FIELDING : has

    PLAYER {
        int player_id PK
        string name
    }

    TEAM {
        int team_id PK
        string name
    }

    ROUND {
        int round_id PK
        string name
    }

    BATTING {
        int batting_id PK
        int player_id FK
        int team_id FK
        int round_id FK
        int games
        int plate_appearances
        int at_bats
        int runs
        int hits
        int home_runs
        int total_bases
        int runs_batted_in
        float batting_average
        int base_on_balls
        int strike_outs
        int hit_by_pitch
        int stolen_bases
        int caught_stealing
        int sacrifice_bunts
        int sacrifice_flies
        float slugging_percentage
        float batting_avg_with_runners_in_scoring_position
    }

    PITCHING {
        int pitching_id PK
        int player_id FK
        int team_id FK
        int round_id FK
        int games
        int wins
        int losses
        int saves
        int holds
        float innings_pitched
        int batters_faced
        int balls
        int strikes
        int runs
        int earned_runs
        float earned_run_average
        int strikeouts
        int hits
        int walks
        int intentional_walks
        int balks
        int wild_pitches
        int home_runs
    }

    FIELDING {
        int fielding_id PK
        int player_id FK
        int team_id FK
        int round_id FK
        int games
        int errors
        int putouts
        int assists
        int stolen_bases_allowed
        int caught_stealing
        int double_plays
        int triple_plays
        int passed_balls
        float fielding_percentage
        float fielding_percentage_pos1
        float fielding_percentage_pos2
        float fielding_percentage_pos3
        float fielding_percentage_pos4
        float fielding_percentage_pos5
        float fielding_percentage_pos6
        float fielding_percentage_pos7
        float fielding_percentage_pos8
        float fielding_percentage_pos9
        float innings_played
    }
```

## Entity Descriptions

### PLAYER
Represents a baseball player with a unique identifier and name.

### TEAM
Represents a baseball team with a unique identifier and name.

### ROUND
Represents a round or period of play in the league.

### BATTING
Tracks batting statistics for players in specific rounds and teams:
- Games played
- Plate appearances
- At-bats
- Runs
- Hits
- Home runs
- Total bases
- Runs batted in
- Batting average
- Base on balls (walks)
- Strikeouts
- Hit by pitch
- Stolen bases
- Caught stealing
- Sacrifice bunts
- Sacrifice flies
- Slugging percentage
- Batting average with runners in scoring position

### PITCHING
Tracks pitching statistics for players in specific rounds and teams:
- Games pitched
- Wins
- Losses
- Saves
- Holds
- Innings pitched
- Batters faced
- Balls thrown
- Strikes thrown
- Runs allowed
- Earned runs
- Earned run average
- Strikeouts
- Hits allowed
- Walks allowed
- Intentional walks
- Balks
- Wild pitches
- Home runs allowed

### FIELDING
Tracks fielding statistics for players in specific rounds and teams:
- Games played
- Errors
- Putouts
- Assists
- Stolen bases allowed
- Caught stealing
- Double plays
- Triple plays
- Passed balls
- Fielding percentage (overall)
- Fielding percentage by position (1-9)
- Innings played

Note: The diagram shows a general relationship model. Position-specific fielding statistics (PO1, A1, etc.) are included in the FIELDING entity but not explicitly shown in the diagram for clarity.