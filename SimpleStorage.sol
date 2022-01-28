// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    // this will get initialized to 0.
    uint256 favoriteNumber;

    // struct with two variables.
    struct People {
        string name;
        uint256 favoriteNumber;
    }

    // this is a dynamic array of empty people.
    People[] public people;

    // this maps from a string (name) to a uint (its favorite number) variable.
    mapping(string => uint256) public nameToFavoriteNumber;

    // this function stores (with gas cost) any number to the uint256's favoriteNumber variable.
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // this function retrieves (with no gas cost because of "VIEW") the uint256's favoriteNumber variable.
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // this function adds the person to the people's array and to the nameToFavoriteNumber's mapping.
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_name, _favoriteNumber));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
