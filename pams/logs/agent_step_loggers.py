from typing import Dict
from typing import List

from .base import Logger
# from .base import MarketStepEndLog
from .base import OrderLog


class AgentOrderLogger(Logger):
    """Logger of the agent order class."""

    def process_order_log(self, log: OrderLog) -> None:
        """print the order log.

        Args:
            log (:class:`pams.logs.OrderLog`): order log.

        Returns:
            None
        """
        print(
            f"{log.order_id} {log.agent_id}" # {log.market.market_id} {log.market.name} {log.market.get_market_price()} {log.market.get_fundamental_price()}"
        )


class AgentOrderSaver(Logger):
    """Saver of the agent order class."""

    agent_order_logs: List[Dict] = []

    def process_order_log(self, log: OrderLog) -> None:
        """stack the order log.

        Args:
            log (:class:`pams.logs.OrderLog`): order log.

        Returns:
            None
        """
        self.agent_order_logs.append(
            {
                  "order_id": log.order_id,
                  "agent_id": log.agent_id,
#                 "session_id": log.session.session_id,
#                 "market_time": log.market.get_time(),
#                 "market_id": log.market.market_id,
#                 "market_name": log.market.name,
#                 "market_price": log.market.get_market_price(),
#                 "fundamental_price": log.market.get_fundamental_price(),
            }
        )
