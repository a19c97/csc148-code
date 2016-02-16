"""Assignment 1 - Grocery Store Models (Task 1)

This file should contain all of the classes necessary to model the entities
in a grocery store.
"""
# This module is used to read in the data from a json configuration file.
import json


class GroceryStore:
    """A grocery store.

    A grocery store should contain customers and checkout lines.

    TODO: make sure you update the documentation for this class to include
    a list of all public and private attributes, in the style found in
    the Class Design Recipe.

    === Public Attributes ===
    @type check_out_lines: LineList
    @type waiting_customers: dict{str: Customer}
    @type finished_customers: dict{str: Customer}
        # Each Customer who has finished checking out will be added
        to this list.
    This list will be used to determine the max waiting time

    """

    def __init__(self, filename):
        """Initialize a GroceryStore from a configuration file <filename>.

        @type filename: str
            The name of the file containing the configuration for the
            grocery store.
        @rtype: None
        """
        with open(filename, 'r') as file:
            config = json.load(file)

            # <config> is now a dictionary with the keys 'cashier_count',
            # 'express_count', 'self_serve_count', and 'line_capacity'.

        self.check_out_lines = LineList(config["cashier_count"],
                                        config["express_count"],
                                        config["self_serve_count"],
                                        config["line_capacity"])
        self.waiting_customers = {}
        self.finished_customers = {}

    def new_customer(self, timestamp, name, items):
        """
        Accepts data for a new customer, creates a new Customer.
        @type self: GroceryStore
        @type name: str
        @type items: int
        @rtype: Customer

        >>> store = GroceryStore('config.json')
        >>> c = store.new_customer(0, 'Jack', 5)
        >>> c.start_waiting
        0
        >>> c.name
        'Jack'
        >>> c.items
        5
        """
        new = Customer(name, items)
        new.start_waiting = timestamp
        self.waiting_customers[new.name] = new
        return new

    def assign_customer(self, customer):
        """
        Assign a Customer to a Line. Returns the number of the Line the Customer
         joined
        @type self: GroceryStore
        @type customer: Customer
        @rtype: int

        >>> store = GroceryStore('config.json')
        >>> customer = Customer('Jack', 5)
        >>> store.assign_customer(customer)
        0
        """
        assigned_line = self.check_out_lines.assign_customer(customer)
        customer.which_line = assigned_line
        self.check_out_lines.lines[assigned_line].add_customer(customer)
        return assigned_line

    def new_join(self, timestamp, name, items):
        """
        Processes the NewArrive event. Return the number of the assigned Line.
        @type self: GroceryStore
        @type name: str
        @type items: int
        @rtype: int

        >>> store = GroceryStore('config.json')
        >>> store.new_join(0, 'Jack', 3)
        0
        """

        if name not in self.waiting_customers:
            assigned_line = \
                self.assign_customer(self.new_customer(timestamp, name, items))
            return assigned_line
        else:
            assigned_line = self.assign_customer(self.waiting_customers[name])
            return assigned_line

    def begin_check_out(self, timestamp, name):
        """
        Processes the Begin event.
        Should return the time it took the current Customer to check out.
        @type self: GroceryStore
        @type name: str
        @rtype: int
        """
        customer = self.waiting_customers[name]
        line_number = customer.which_line
        line = self.check_out_lines.lines[line_number]
        check_out_time = line.get_check_out_time(customer)
        return check_out_time

    def finish_check_out(self, timestamp, name):
        """
        Processes the Finish event.
        Should return the name of the next Customer in this Line.
        @type self: GroceryStore
        @type timestamp: int
        @type name: str
        @rtype: str
        """

        customer = self.waiting_customers[name]
        customer.end_waiting = timestamp
        self.finished_customers[customer.name] = customer
        current_line = self.check_out_lines.lines[customer.which_line]
        current_line.customers.pop(0)
        if not len(current_line.customers) == 0:
            next_name = \
                self.check_out_lines.lines[customer.which_line].customers[
                    0].name
            return next_name
        else:
            return None

    def close_line(self, timestamp, which_line):
        """
        Processes the CloseLine event.
        Returns a list of customers who have to be reassigend.
        @type self: GroceryStore
        @type timestamp: int
        @type which_line: int
        @rtype: list[Customer]
        """
        closed_line = self.check_out_lines.lines[which_line]
        closed_line.closed = True
        return_customers = []
        while len(closed_line.customers) > 1:
            current_customer = closed_line.customers.pop()
            assigned_line = self.assign_customer(current_customer)
            current_customer.which_line = assigned_line
            return_customers.append(current_customer)
        return return_customers


class Customer:
    """
    One single customer.

    === Public attributes ===
    @type name: str
    @type items: int
    @type start_waiting: int
    @type end_waiting: int
    @type which_line: int

    """

    def __init__(self, name, items):
        """
        Initializes a Customer object.
        @type self: Customer
        @type name: str
        @type items: int
        @rtype: None

        >>> a = Customer('Jack', 3)
        >>> a.name
        'Jack'
        >>> a.items
        3
        """
        self.name = name
        self.items = items
        self.start_waiting = 0
        self.end_waiting = 0
        self.which_line = -1

    def get_wait_time(self):
        """
        Returns how long this Customer has been waiting.
        @type self: Customer
        @rtype: int

        >>> a = Customer('Jack', 3)
        >>> a.get_wait_time()
        0
        """
        return self.end_waiting - self.start_waiting


class Line:
    """
    An abstract class to model a check out line.
    A Line essentially stores a list of Customers.

    === Public attributes ===
    @type closed: bool # keeps track of if the line is closed
    @type customers: [Customer]
    @type capacity: int # the max number of customers a line can have
    @type is_express_line: bool
    """

    def __init__(self, capacity, is_express_line):
        """
        Initializes a Line object.
        @type self: Line
        @type capacity: int
        @type is_express_line: bool

        >>> this_line = Line(10, True)
        >>> this_line.capacity
        10
        >>> this_line.is_express_line
        True
        >>> this_line.closed
        False
        """
        self.customers = []
        self.capacity = capacity
        self.closed = False
        self.is_express_line = is_express_line

    def can_add_customer(self, customer):
        """
        Returns True if a Customer can be added to this line.
        @type self: Line
        @type customer: Customer
        @rtype: bool

        >>> this_line = Line(10, True)
        >>> customer = Customer('Jack', 3)
        >>> this_line.can_add_customer(customer)
        True
        """
        if len(self.customers) >= self.capacity:
            return False
        elif self.closed:
            return False
        elif self.is_express_line:
            if customer.items >= 8:
                return False
            else:
                return True
        else:
            return True

    def add_customer(self, customer):
        """
        Adds a customer to a line.
        Returns True if the Customer is added successfully.
        @type self: Line
        @type customer: Customer
        @rtype: bool

        >>> this_line = Line(10, True)
        >>> customer = Customer('Jack', 3)
        >>> this_line.add_customer(customer)
        True
        """
        self.customers.append(customer)
        return True

    def get_check_out_time(self, customer):
        """
        Returns the time it takes for a Customer to check out at a Line.
        To be implemented in respective subcalsses.
        @type self: Line
        @type customer: Customer
        @rtype: int
        """
        raise NotImplementedError


class CashierLine(Line):
    """
    A cashier line
    Takes n + 7 seconds for each customer to check out.
    """

    def __init__(self, capacity, is_express_line):
        """
        Initializes a CashierLine.
        @type self: CashierLine
        @type capacity: int
        @type is_express_line: bool
        @rtype: None

        >>> this_line = CashierLine(10, False)
        >>> this_line.capacity
        10
        >>> this_line.is_express_line
        False
        """
        super(CashierLine, self).__init__(capacity, is_express_line)

    def get_check_out_time(self, customer):
        """
        Implements the get_check_out_time method in super.
        @type self: CashierLine
        @type customer: Customer
        @rtype int

        >>> this_line = CashierLine(10, False)
        >>> customer = Customer('Jack', 3)
        >>> this_line.get_check_out_time(customer)
        10
        """
        return customer.items + 7


class ExpressLine(Line):
    """
    An express line
    Takes n + 4 seconds for each Customer to check out.
    Customers can only enter this line if they have fewer than 8 items.
    """

    def __init__(self, capacity, is_express_line):
        """
        Initializes an ExpressLine.
        @type self: ExpressLine
        @type capacity: int
        @type is_express_line: bool
        @rtype: None

        >>> this_line = ExpressLine(10, True)
        >>> this_line.capacity
        10
        >>> this_line.is_express_line
        True
        """
        super(ExpressLine, self).__init__(capacity, is_express_line)

    def get_check_out_time(self, customer):
        """
        Implements the get_check_out_time method in super.
        @type self: ExpressLine
        @type customer: Customer
        @rtype int

        >>> this_line = ExpressLine(10, True)
        >>> customer = Customer('Jack', 3)
        >>> this_line.get_check_out_time(customer)
        7
        """
        return customer.items + 4


class SelfServeLine(Line):
    """
    A self serve line
    Takes 2n+1 seconds for each Customer to check out.
    """

    def __init__(self, capacity, is_express_line):
        """
        Initializes an SelfServeLine.
        @type self: SelfServeLine
        @type capacity: int
        @type is_express_line: bool
        @rtype: None

        >>> this_line = SelfServeLine(10, False)
        >>> this_line.capacity
        10
        >>> this_line.is_express_line
        False
        """
        super(SelfServeLine, self).__init__(capacity, is_express_line)

    def get_check_out_time(self, customer):
        """
        Implements the get_check_out_time method in super.
        @type self: SelfServeLine
        @type customer: Customer
        @rtype int

        >>> this_line = SelfServeLine(10, False)
        >>> customer = Customer('Jack', 4)
        >>> this_line.get_check_out_time(customer)
        9
        """
        return customer.items * 2 + 1


class LineList:
    """
    A list of check out lines.
    === Public attributes ===
    @type lines: list[Line]
    """

    def __init__(self, cashier, express, self_serve, capacity):
        """
        Initializes a LineList.
        @type self: LineList
        @type cashier: int
        @type express: int
        @type self_serve: int
        @type capacity: int
        @rtype: None
        """
        self.lines = []
        for x in range(cashier):
            self.lines.append(CashierLine(capacity, False))
        for x in range(express):
            self.lines.append(ExpressLine(capacity, True))
        for x in range(self_serve):
            self.lines.append(SelfServeLine(capacity, False))

    def assign_customer(self, customer):
        """
        Returns which line a Customer should be assigned to.
        @type self: LineList
        @type customer: Customer
        @rtype: int

        >>> check_out_lines = LineList(1, 0, 0, 10)
        >>> customer = Customer('Jack', 3)
        >>> check_out_lines.assign_customer(customer)
        0
        """
        minimum = self.lines[0].capacity
        line = -1
        for x in range(len(self.lines)):
            if self.lines[x].can_add_customer(customer):
                if len(self.lines[x].customers) < minimum:
                    minimum = len(self.lines[x].customers)
                    line = x
        return line

# You can run a basic test here using the default 'config.json'
# file we provided.
if __name__ == '__main__':
    store = GroceryStore('config.json')
    # Execute some methods here
    import doctest
    doctest.testmod()
