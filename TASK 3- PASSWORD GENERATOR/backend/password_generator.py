import random
import string

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_special=True):
        character_set = self.lowercase
        
        if use_uppercase:
            character_set += self.uppercase
        if use_digits:
            character_set += self.digits
        if use_special:
            character_set += self.special_chars
        
        # Ensure password contains at least one character from each selected set
        password = []
        if use_uppercase:
            password.append(random.choice(self.uppercase))
        if use_digits:
            password.append(random.choice(self.digits))
        if use_special:
            password.append(random.choice(self.special_chars))
        
        # Fill the rest of the password
        remaining_length = length - len(password)
        password.extend(random.choice(character_set) for _ in range(remaining_length))
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password)
        
        return ''.join(password)
    
    def _evaluate_strength(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        score = 0
        # Length score
        if length >= 12: score += 3
        elif length >= 8: score += 2
        else: score += 1
        
        # Complexity score
        complexity = sum([has_upper, has_lower, has_digit, has_special])
        score += complexity
        
        # Evaluate strength
        if score >= 6: return "Very Strong"
        if score >= 4: return "Strong"
        if score >= 3: return "Moderate"
        return "Weak"

# Command-line interface
if __name__ == "__main__":
    print("=== Password Generator ===")
    try:
        length = int(input("Enter password length (8-64): "))
        if length < 8 or length > 64:
            raise ValueError("Password length should be between 8 and 64")
        
        use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
        use_digits = input("Include digits? (y/n): ").lower() == 'y'
        use_special = input("Include special characters? (y/n): ").lower() == 'y'
        
        generator = PasswordGenerator()
        password = generator.generate_password(
            length=length,
            use_uppercase=use_upper,
            use_digits=use_digits,
            use_special=use_special
        )
        
        print("\nGenerated Password:")
        print(password)
        print("\nPassword strength:", generator._evaluate_strength(password))
        
    except ValueError as e:
        print(f"Error: {e}")