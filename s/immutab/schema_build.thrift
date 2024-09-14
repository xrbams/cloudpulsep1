union PlayerID {
  1: string nickname;
  2: i64 player_id;
}

union TeamID {
  1: string team_name;
}

struct EquivEdge {
  1: required PlayerID id1;
  2: required PlayerID id2;
}

struct TeamMembershipEdge {
  1: required PlayerID player;
  2: required TeamID team;
  3: required i64 joined_date;
}

struct Location {
  1: optional string city;
  2: optional string state;
  3: optional string country;
}

enum GenderType {
  MALE = 1,
  FEMALE = 2
}

union PlayerPropertyValue {
  1: string full_name;
  2: GenderType gender;
  3: Location location;
  4: i16 age;
}

struct PlayerProperty {
  1: required PlayerID id;
  2: required PlayerPropertyValue property;
}

union TeamPropertyValue {
  1: i32 championships_won;
}

struct TeamProperty {
  1: required TeamID id;
  2: required TeamPropertyValue property;
}

union DataUnit {
  1: PlayerProperty player_property;
  2: TeamProperty team_property;
  3: EquivEdge equiv;
  4: TeamMembershipEdge team_membership;
}

struct Pedigree {
  1: required i32 true_as_of_secs;
}

struct Data {
  1: required Pedigree pedigree;
  2: required DataUnit dataunit;
}

union PlayerPropertyValue {
  1: string full_name;
  2: GenderType gender;
  3: Location location;
  4: i16 age;
  5: i32 rank; // New field added
}

struct PlayerTransferEdge {
  1: required PlayerID player;
  2: required TeamID from_team;
  3: required TeamID to_team;
  4: required i64 transfer_date;
}

union DataUnit {
  1: PlayerProperty player_property;
  2: TeamProperty team_property;
  3: EquivEdge equiv;
  4: TeamMembershipEdge team_membership;
  5: PlayerTransferEdge player_transfer; // New edge added
}
