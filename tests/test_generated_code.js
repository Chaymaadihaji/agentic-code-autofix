const { soustraire } = require('./solution');

describe('soustraire', () => {
    it('soustraire 5 et 3', () => {
        expect(soustraire(5, 3)).toBe(2);
    });

    it('soustraire 10 et 7', () => {
        expect(soustraire(10, 7)).toBe(3);
    });

    it('soustraire -5 et 3', () => {
        expect(soustraire(-5, 3)).toBe(-8);
    });

    it('soustraire 0 et 0', () => {
        expect(soustraire(0, 0)).toBe(0);
    });

    it('soustraire -10 et -7', () => {
        expect(soustraire(-10, -7)).toBe(-3);
    });
});