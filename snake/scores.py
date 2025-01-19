# Standard library imports
from pathlib import Path
import typing

# Third-party imports
import schema
import yaml

# Local imports
from .score import Score

SCORE_FILE_SCHEMA = schema.Schema([
    {"name":str,
     "score":int}
])

class Scores :
    """Contains the instances of scores."""

    def __init__(self, max_scores : int, scores : list[Score]) -> None :
        """Definition of scores."""
        self._max_scores=max_scores
        self._scores=sorted(scores, reverse = True)[:max_scores]

    @classmethod
    def default(cls, max_scores : int ) -> "Scores" :
        """Classmethod."""
        return cls(max_scores,
                   [Score (score=1,name="Carly"),
                    Score(score=2,name="Donald"),
                    Score(score=3,name="Stacy"),
                    Score(score=4,name="James")])

    def __iter__(self) -> typing.Iterator[Score]:
        """Iterate on the scores list."""
        return iter(self._scores)


    def is_highscore(self, score_player : int) -> bool :
        """Define the case highscore."""
        return len(self._scores)<self._max_scores or self._scores[-1].score < score_player

    def add_score(self, score_player: Score) -> None:
        """Add a score and sort the list."""
        if self.is_highscore(score_player.score):
            if len(self._scores)>=self._max_scores :
                self._scores.pop()
            self._scores.append(score_player)
            self._scores.sort(reverse=True)

    def saving_hs(self,hs_file:Path)->None:
        """Save high score into the file."""
        high_scores=[{"name":s.name,"score":s.score} for s in self]
        with hs_file.open("w") as fd:
            yaml.safe_dump(high_scores,fd)

    def loading_hs(self,scores_file:Path) -> None:
        """Load high scores from the file."""
        with open(scores_file, "r") as f:
            hs = yaml.load(f, Loader=yaml.Loader)
        SCORE_FILE_SCHEMA.validate(hs)
        self._scores=[]
        for sc in hs:
            self._scores.append(Score(sc["score"],sc["name"]))
        self._scores=sorted(self._scores, reverse = True)[:self._max_scores]















