// SPDX-License-Identifier: MIT 
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";


contract PlayerTokenNFT is ERC721, ERC721Enumerable, Pausable, Ownable {
    string private baseURIExtended;
    uint256 public immutable MAX_SUPPLY;

    constructor(
        // string memory _name,
        // string memory _symbol,
        // string memory _uri,
        // uint256 maxSupply
    ) payable ERC721("PlayerTokenNFT", "PLYTKN") {
        baseURIExtended = 'http://localhost:3000/playtoken/meta/';
        MAX_SUPPLY = 1_000_000;
        pause();
    }

    function pause() internal {
        _pause();
    }

    function mint(address _to) external onlyOwner {
        uint256 _totalSupply = totalSupply();
        require(_totalSupply + 1 <= MAX_SUPPLY, "Mint would exceed maximum supply");
        _safeMint(_to, _totalSupply);
    }

    function setBaseURI(string memory baseURI_) external onlyOwner {
        baseURIExtended = baseURI_;
    }

    // Overrides
    function _baseURI() internal view virtual override returns (string memory ) {
        return baseURIExtended;
    }

    function _beforeTokenTransfer(
        address _from,
        address _to,
        uint256 _tokenId,
        uint256 _batchSupply
    ) internal override (ERC721, ERC721Enumerable) {
        require(_msgSender() == owner() && paused(), "not owner cannot mint");
        super._beforeTokenTransfer(_from, _to, _tokenId, _batchSupply);
    }

    function supportsInterface(bytes4 _interfaceId)
        public 
        view 
        override (ERC721, ERC721Enumerable)
        returns (bool) 
    {
        return super.supportsInterface(_interfaceId);
    }
}